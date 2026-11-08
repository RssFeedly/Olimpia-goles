import feedparser
import requests
from feedgen.feed import FeedGenerator

# URL original del canal de YouTube
TARGET_YOUTUBE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCDnZ8zbVWLaVfuDmNuWq7rw"

# Usamos un proxy web gratuito para evitar el bloqueo HTTP 500 de YouTube en GitHub Actions
SOURCE_RSS = f"https://api.allorigins.win/raw?url={requests.utils.quote(TARGET_YOUTUBE_RSS)}"

KEYWORDS = [
    "Olimpia",
    "olimpia",
]

print(f"[*] Conectando mediante proxy con el RSS de YouTube...")
try:
    response = requests.get(SOURCE_RSS, timeout=30)
    print(f"[*] Código de respuesta HTTP: {response.status_code}")
except Exception as e:
    print(f"[!] Error al realizar la petición HTTP: {e}")
    exit(1)

feed = feedparser.parse(response.content)
print(f"[*] Total de entradas encontradas en el RSS: {len(feed.entries)}")

fg = FeedGenerator()
fg.title("RSS Filtrado - Olimpia")
fg.link(href="https://www.youtube.com/channel/UCDnZ8zbVWLaVfuDmNuWq7rw")
fg.description("Videos filtrados de YouTube para Olimpia")

added_count = 0

for entry in feed.entries:
    title = entry.get("title", "").strip()
    link = entry.get("link", "")
    
    print(f" -> Evaluando título: '{title}'")

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
fg.rss_file("feed.xml")
print("[*] Archivo feed.xml generado correctamente.")
