import feedparser
import requests
from feedgen.feed import FeedGenerator

# Usamos la URL estándar de YouTube que suele funcionar en canales estables
SOURCE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCDnZ8zbVWLaVfuDmNuWq7rw"

KEYWORDS = [
    "Olimpia",
    "olimpia",
]

# Cabeceras limpias que utilizas en tus otros scripts funcionales
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"[*] Descargando feed oficial de YouTube...")
try:
    response = requests.get(SOURCE_RSS, headers=headers, timeout=30)
    print(f"[*] Código de respuesta HTTP: {response.status_code}")
except Exception as e:
    print(f"[!] Error HTTP: {e}")
    exit(1)

feed = feedparser.parse(response.content)
print(f"[*] Total de entradas encontradas: {len(feed.entries)}")

fg = FeedGenerator()
fg.title("RSS Filtrado - Olimpia")
fg.link(href=SOURCE_RSS)
fg.description("Videos filtrados de YouTube para Olimpia")

added_count = 0

for entry in feed.entries:
    title = entry.get("title", "").strip()
    link = entry.get("link", "")
    
    print(f" -> Evaluando: '{title}'")

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

print(f"[*] Total de videos agregados: {added_count}")
fg.rss_file("feed.xml")
print("[*] Archivo feed.xml generado correctamente.")
