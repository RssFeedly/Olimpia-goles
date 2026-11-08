import feedparser
import requests
from feedgen.feed import FeedGenerator

SOURCE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCDnZ8zbVWLaVfuDmNuWq7rw"

# Puedes añadir variaciones por seguridad (sin tildes, en minúsculas, etc.)
KEYWORDS = [
    "olimpia",
]

# Cabeceras completas para evitar que YouTube bloquee la petición de GitHub Actions
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
}

print(f"[*] Conectando con el canal de YouTube...")
try:
    response = requests.get(SOURCE_RSS, headers=headers, timeout=30)
    print(f"[*] Código de respuesta HTTP: {response.status_code}")
except Exception as e:
    print(f"[!] Error al realizar la petición HTTP: {e}")
    exit(1)

# Parseamos el contenido XML obtenido
feed = feedparser.parse(response.content)
print(f"[*] Total de entradas encontradas en el RSS original: {len(feed.entries)}")

fg = FeedGenerator()
fg.title("RSS Filtrado - Olimpia")
fg.link(href=SOURCE_RSS)
fg.description("Videos filtrados de YouTube para Olimpia")

added_count = 0

for entry in feed.entries:
    title = entry.get("title", "").strip()
    link = entry.get("link", "")
    
    # Imprimimos cada título evaluado para verlo en los logs de GitHub Actions
    print(f" -> Evaluando título: '{title}'")

    # Verificamos si alguna keyword está contenida en el título (ignorando mayúsculas/minúsculas)
    if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=link)

        if hasattr(entry, "published"):
            fe.pubDate(entry.published)

        if hasattr(entry, "summary"):
            fe.description(entry.summary)
            
        print(f"    [MATCH] ¡Añadido al feed!")
        added_count += 1

print(f"[*] Total de videos agregados tras el filtrado: {added_count}")

# Generamos el archivo XML final
fg.rss_file("feed.xml")
print("[*] Archivo feed.xml generado correctamente.")
