from fastapi import FastAPI
import requests, random, time
from bs4 import BeautifulSoup

from fastapi.middleware.cors import CORSMiddleware 


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["https://yourwebsite.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Remote server where GIFs are hosted (must allow directory listing or have index.html)
#REMOTE_FOLDER = "http://127.0.0.1:8181/gifs/"  # <-- change this to your server URL
REMOTE_FOLDER = "https://hyndzia.xyz/gifs/"  # <-- change this to your server URL


# Cache settings
CACHE = {"gifs": [], "last_update": 0}
CACHE_TTL = 1000  # refresh every 60s

def fetch_remote_gifs():
    """
    Scrape the remote folder and return all .gif links.
    """
    try:
        response = requests.get(REMOTE_FOLDER, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        gifs = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".gif"):
                # Handle relative vs absolute paths
                if href.startswith("http"):
                    gifs.append(href)
                else:
                    gifs.append(REMOTE_FOLDER.rstrip("/") + "/" + href.lstrip("/"))
        return gifs
    except Exception as e:
        print(f"Error fetching GIFs: {e}")
        return []

def get_cached_gifs():
    """
    Get cached GIF list, refresh if cache expired.
    """
    now = time.time()
    if now - CACHE["last_update"] > CACHE_TTL or not CACHE["gifs"]:
        CACHE["gifs"] = fetch_remote_gifs()
        CACHE["last_update"] = now
    return CACHE["gifs"]

# @app.get("/list_gifs")
# def list_gifs():
#     """
#     Return the full list of GIFs.
#     """
#     gifs = get_cached_gifs()
#     return {"gifs": gifs}

@app.get("/random_gif")
def random_gif():
    """
    Return a random GIF URL from the remote folder.
    """
    gifs = get_cached_gifs()
    if not gifs:
        return {"error": "No GIFs available"}
    return {"gif": random.choice(gifs)}

