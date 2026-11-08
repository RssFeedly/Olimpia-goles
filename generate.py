import feedparser
import requests
from feedgen.feed import FeedGenerator

SOURCE_RSS = "https://rsshub.app/youtube/channel/UCDnZ8zbVWLaVfuDmNuWq7rw"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

print(f"[*] Conectando con RSSHub...")
response = requests.get(SOURCE_RSS, headers=headers, timeout=30)
feed = feedparser.parse(response.content)

print(f"[*] Total de entradas encontradas: {len(feed.entries)}")

fg = FeedGenerator()
fg.title("RSS Filtrado - Olimpia")
fg.link(href="https://www.youtube.com/channel/UCDnZ8zbVWLaVfuDmNuWq7rw")
fg.description("Videos filtrados de YouTube para Olimpia")

# REVISIÓN TOTAL: Vamos a añadir temporalmente CUALQUIER video para ver qué títulos lee
for entry in feed.entries:
    title = entry.get("title", "").strip()
    link = entry.get("link", "")
    
    # Imprime cada título en los logs de GitHub sin filtrar nada
    print(f" -> TÍTULO LEÍDO: '{title}'")

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=link)

    if hasattr(entry, "published"):
        fe.pubDate(entry.published)

    if hasattr(entry, "summary"):
        fe.description(entry.summary)

fg.rss_file("feed.xml")
print("[*] Archivo feed.xml generado con todos los videos recientes.")
