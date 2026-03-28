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
    from browser_use import Agent, Browser, BrowserConfig
    from langchain_anthropic import ChatAnthropic

    url = CATALOGHI.get(catalogo)
    if not url:
        return {"errore": f"Catalogo '{catalogo}' non supportato. Scegli tra: {list(CATALOGHI.keys())}"}

    llm = ChatAnthropic(
        model="claude-3-5-haiku-20241022",
        api_key=Config.ANTHROPIC_API_KEY,
    )

    task = (
        f"Vai su {url} e cerca il prodotto: '{query}'. "
        "Per ogni risultato trovato estrai queste informazioni: "
        "titolo/nome prodotto, codice articolo o codice OE, prezzo (se visibile). "
        "Restituisci i risultati come lista JSON con campi: titolo, codice, prezzo."
    )

    agent = Agent(task=task, llm=llm, browser=Browser(config=BrowserConfig(headless=Config.BROWSER_HEADLESS)))

    try:
        history = await agent.run(max_steps=20)
        risultati = history.final_result() or "Nessun risultato trovato."
        return {
            "catalogo": catalogo,
            "query": query,
            "risultati": risultati,
        }
    except Exception as e:
        return {
            "catalogo": catalogo,
            "query": query,
            "errore": str(e),
        }


async def accedi_portale_b2b(portale: str, obiettivo: str) -> dict:
    """
    Accede a un portale B2B usando le credenziali salvate nel .env e completa
    l'obiettivo specificato. L'agente NON chiede credenziali in chat.

    portale: chiave del portale (es: 'azcar', 'elring', 'corteco', 'valeo', 'autodoc')
    obiettivo: cosa fare dopo il login (es: 'cerca filtri olio BMW Serie 3 e restituisci prezzi')
    """
    from browser_use import Agent, Browser, BrowserConfig
    from langchain_anthropic import ChatAnthropic

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

    task_parts.append(obiettivo)
    task_parts.append("Rispondi in italiano con i dati trovati.")

    llm = ChatAnthropic(
        model="claude-3-5-haiku-20241022",
        api_key=Config.ANTHROPIC_API_KEY,
    )

    agent = Agent(task=" ".join(task_parts), llm=llm, browser=Browser(config=BrowserConfig(headless=Config.BROWSER_HEADLESS)))

    try:
        history = await agent.run(max_steps=30)
        return {
            "portale": info["nome"],
            "risultato": history.final_result() or "Nessun risultato.",
        }
    except Exception as e:
        return {"portale": info["nome"], "errore": str(e)}


async def naviga_web(url: str, obiettivo: str) -> dict:
    """
    Naviga qualsiasi URL con browser-use ed esegue l'obiettivo specificato.
    Uso generale: analizzare siti competitor, estrarre strutture, leggere pagine.

    Esempi:
      naviga_web("https://www.autodoc.it", "Elenca le categorie principali del sito")
      naviga_web("https://www.elring.de/it", "Trova i prodotti per BMW N47 con prezzi")
    """
    from browser_use import Agent, Browser, BrowserConfig
    from langchain_anthropic import ChatAnthropic

    llm = ChatAnthropic(
        model="claude-3-5-haiku-20241022",
        api_key=Config.ANTHROPIC_API_KEY,
    )

    agent = Agent(
        task=f"Vai su {url}. {obiettivo} Rispondi in italiano con i dati trovati.",
        llm=llm,
        browser=Browser(config=BrowserConfig(headless=Config.BROWSER_HEADLESS)),
    )

    try:
        history = await agent.run(max_steps=25)
        return {"url": url, "risultato": history.final_result() or "Nessun risultato."}
    except Exception as e:
        return {"url": url, "errore": str(e)}


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
