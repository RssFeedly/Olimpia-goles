import feedparser
import requests
from feedgen.feed import FeedGenerator

SOURCE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCDnZ8zbVWLaVfuDmNuWq7rw"

KEYWORDS = [
    "Olimpia",
]

# Cabeceras para simular un navegador y evitar bloqueos de YouTube en GitHub Actions
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"Descargando feed de: {SOURCE_RSS}")
response = requests.get(SOURCE_RSS, headers=headers, timeout=30)
print(f"Código de estado HTTP: {response.status_code}")

feed = feedparser.parse(response.text)
print(f"Total de videos encontrados en el canal de YouTube: {len(feed.entries)}")

fg = FeedGenerator()
fg.title("RSS Filtrado")
fg.link(href=SOURCE_RSS)
fg.description("Videos filtrados de YouTube")

added_count = 0
for entry in feed.entries:
    title = entry.title
    print(f"Revisando video: {title}")

    if any(k.lower() in title.lower() for k in KEYWORDS):
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=entry.link)

        if hasattr(entry, "published"):
            fe.pubDate(entry.published)

        if hasattr(entry, "summary"):
            fe.description(entry.summary)
            
        added_count += 1

print(f"Videos añadidos tras el filtro: {added_count}")
fg.rss_file("feed.xml")
print("Archivo feed.xml generado con éxito.")
