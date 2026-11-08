import feedparser
import requests
from feedgen.feed import FeedGenerator

# Usamos RSSHub como pasarela gratuita para evitar el bloqueo de IP de YouTube en GitHub Actions
SOURCE_RSS = "https://rsshub.app/youtube/channel/UCDnZ8zbVWLaVfuDmNuWq7rw"

KEYWORDS = [
    "olimpia",
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

print(f"[*] Conectando mediante proxy RSS con el canal de YouTube...")
try:
    response = requests.get(SOURCE_RSS, headers=headers, timeout=30)
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
