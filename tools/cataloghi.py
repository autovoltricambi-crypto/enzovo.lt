"""Ricerca cataloghi B2B usando browser-use + sessione HTTP per WordPress."""
import asyncio
import httpx
from config import Config

# Sessione HTTP per WordPress (inizializzata all'avvio del server)
_wp_client: httpx.AsyncClient | None = None

CATALOGHI = {
    "Elring": "https://www.elring.de",
    "Corteco": "https://www.corteco.com",
    "Valeo": "https://www.valeo.com",
    "AutoDoc": "https://www.autodoc.it",
}


def _browser_model_chain() -> list[str]:
    """Ritorna la catena modelli browser-use senza duplicati."""
    chain = []
    for model in (
        Config.BROWSER_MODEL_PRIMARY,
        Config.BROWSER_MODEL_SECONDARY,
        Config.BROWSER_MODEL_FALLBACK,
    ):
        model = (model or "").strip()
        if model and model not in chain:
            chain.append(model)
    return chain


def _max_steps_for_model(model_name: str, requested_max_steps: int) -> int:
    """Limita i passi per contenere i costi sui modelli piu economici."""
    model_lower = model_name.lower()
    if "haiku" in model_lower:
        return min(requested_max_steps, 8)
    if "4-0" in model_lower or "sonnet-4" in model_lower:
        return min(requested_max_steps, 18)
    return requested_max_steps


async def _run_browser_agent_with_fallback(task: str, max_steps: int) -> dict:
    """Esegue browser-use provando piu modelli in ordine di fallback."""
    from browser_use import Agent, Browser, BrowserProfile, ChatAnthropic

    profile = BrowserProfile(
        headless=Config.BROWSER_HEADLESS,
        wait_for_network_idle_page_load_time=5,
        **({"user_data_dir": Config.CHROME_USER_DATA_DIR, "profile_directory": Config.CHROME_PROFILE}
           if Config.CHROME_USER_DATA_DIR else {}),
    )

    tentativi = []
    ultimo_errore = None

    for model_name in _browser_model_chain():
        model_steps = _max_steps_for_model(model_name, max_steps)
        llm_kwargs = {"model": model_name, "api_key": Config.ANTHROPIC_API_KEY}
        if "haiku" not in model_name:
            llm_kwargs["model_kwargs"] = {"thinking": {"type": "disabled"}}

        llm = ChatAnthropic(**llm_kwargs)
        browser = Browser(browser_profile=profile)
        agent = Agent(task=task, llm=llm, browser=browser)

        try:
            history = await agent.run(max_steps=model_steps)
            try:
                result = history.final_result()
            except Exception:
                result = None
            return {
                "successo": True,
                "modello_usato": model_name,
                "max_steps_usati": model_steps,
                "risultato": result or "Navigazione completata. Nessun risultato finale estratto.",
                "tentativi": tentativi,
            }
        except Exception as e:
            ultimo_errore = str(e)
            tentativi.append({"modello": model_name, "max_steps": model_steps, "errore": str(e)})
        finally:
            try:
                await browser.close()
            except Exception:
                pass

    return {
        "successo": False,
        "errore": ultimo_errore or "Browser-use fallito senza dettagli.",
        "tentativi": tentativi,
    }


# ==========================================
# BROWSER / SESSIONE WORDPRESS
# ==========================================

async def browser_login_wp() -> bool:
    """
    Inizializza la sessione HTTP autenticata verso WordPress REST API.
    Usa Application Passwords (Basic Auth) — nessun browser necessario.
    """
    global _wp_client
    _wp_client = httpx.AsyncClient(
        base_url=Config.WP_URL,
        auth=(Config.WP_USER, Config.WP_PASSWORD),
        timeout=30,
        follow_redirects=True,
    )
    try:
        r = await _wp_client.get("/wp-json/wp/v2/users/me")
        return r.status_code == 200
    except Exception:
        # Server non raggiungibile — teniamo il client per riprovare dopo
        return False


async def browser_chiudi():
    """Chiude la sessione HTTP WordPress."""
    global _wp_client
    if _wp_client:
        await _wp_client.aclose()
        _wp_client = None


def get_wp_client() -> httpx.AsyncClient:
    """Ritorna il client HTTP WordPress. Lancia errore se non inizializzato."""
    if not _wp_client:
        raise RuntimeError(
            "Sessione WordPress non inizializzata. "
            "Assicurati che il server sia avviato correttamente."
        )
    return _wp_client


# ==========================================
# RICERCA CATALOGHI CON BROWSER-USE
# ==========================================

async def cerca_catalogo(catalogo: str, query: str) -> dict:
    """
    Cerca un prodotto su un catalogo B2B usando browser-use.
    browser-use naviga il sito con un browser reale e Claude estrae i dati.
    """
    url = CATALOGHI.get(catalogo)
    if not url:
        return {"errore": f"Catalogo '{catalogo}' non supportato. Scegli tra: {list(CATALOGHI.keys())}"}

    task = (
        f"Vai su {url} e cerca il prodotto: '{query}'. "
        "Per ogni risultato trovato estrai queste informazioni: "
        "titolo/nome prodotto, codice articolo o codice OE, prezzo (se visibile). "
        "Restituisci i risultati come lista JSON con campi: titolo, codice, prezzo."
    )

    run = await _run_browser_agent_with_fallback(task=task, max_steps=20)
    if not run.get("successo"):
        return {
            "catalogo": catalogo,
            "query": query,
            "errore": run.get("errore"),
            "tentativi": run.get("tentativi", []),
            "successo": False,
        }

    return {
        "catalogo": catalogo,
        "query": query,
        "risultati": str(run.get("risultato")),
        "modello_usato": run.get("modello_usato"),
        "tentativi": run.get("tentativi", []),
        "successo": True,
    }


async def accedi_portale_b2b(portale: str, obiettivo: str) -> dict:
    """
    Accede a un portale B2B usando le credenziali salvate nel .env e completa
    l'obiettivo specificato. L'agente NON chiede credenziali in chat.

    portale: chiave del portale (es: 'azcar', 'elring', 'corteco', 'valeo', 'autodoc')
    obiettivo: cosa fare dopo il login (es: 'cerca filtri olio BMW Serie 3 e restituisci prezzi')
    """
    portale_key = portale.lower().replace(" ", "")
    info = Config.PORTALI_B2B.get(portale_key)

    if not info:
        disponibili = list(Config.PORTALI_B2B.keys())
        return {"errore": f"Portale '{portale}' non configurato. Disponibili: {disponibili}"}

    if not info["url"]:
        return {"errore": f"URL per '{portale}' non configurato nel .env"}

    # Costruisce il task con credenziali iniettate — l'agente non le mostra in chat
    task_parts = [f"Vai su {info['url']}."]

    if info["user"] and info["password"]:
        task_parts.append(
            f"Se richiesto, accedi con username '{info['user']}' e password '{info['password']}'. "
            "Non chiedere conferma all'utente."
        )

    task_parts.append("Dopo il login, prendi uno screenshot della home e dimmi esattamente cosa vedi nella pagina.")
    task_parts.append("Se ci sono errori, elementi che non riesci a identificare, o qualsiasi problema, spiegami nel dettaglio cosa succede e perche non puoi continuare.")
    task_parts.append(obiettivo)
    task_parts.append("Rispondi in italiano con i dati trovati.")

    run = await _run_browser_agent_with_fallback(task=" ".join(task_parts), max_steps=30)
    if not run.get("successo"):
        return {
            "portale": info["nome"],
            "errore": run.get("errore"),
            "tentativi": run.get("tentativi", []),
            "successo": False,
        }

    return {
        "portale": info["nome"],
        "risultato": str(run.get("risultato")),
        "modello_usato": run.get("modello_usato"),
        "tentativi": run.get("tentativi", []),
        "successo": True,
    }


async def naviga_web(url: str, obiettivo: str) -> dict:
    """
    Naviga qualsiasi URL con browser-use ed esegue l'obiettivo specificato.
    Uso generale: analizzare siti competitor, estrarre strutture, leggere pagine.

    Esempi:
      naviga_web("https://www.autodoc.it", "Elenca le categorie principali del sito")
      naviga_web("https://www.elring.de/it", "Trova i prodotti per BMW N47 con prezzi")
    """
    run = await _run_browser_agent_with_fallback(
        task=f"Vai su {url}. {obiettivo} Rispondi in italiano con i dati trovati.",
        max_steps=25,
    )
    if not run.get("successo"):
        return {"url": url, "errore": run.get("errore"), "tentativi": run.get("tentativi", []), "successo": False}

    return {
        "url": url,
        "risultato": str(run.get("risultato")),
        "modello_usato": run.get("modello_usato"),
        "tentativi": run.get("tentativi", []),
        "successo": True,
    }


async def cerca_tutti_cataloghi(query: str) -> dict:
    """
    Cerca su tutti i cataloghi in parallelo.
    Ogni catalogo viene cercato in contemporanea per massimizzare la velocità.
    """
    tasks = [cerca_catalogo(cat, query) for cat in CATALOGHI]
    risultati = await asyncio.gather(*tasks, return_exceptions=True)

    output = []
    for r in risultati:
        if isinstance(r, Exception):
            output.append({"errore": str(r)})
        else:
            output.append(r)

    return {"query": query, "cataloghi": output}
