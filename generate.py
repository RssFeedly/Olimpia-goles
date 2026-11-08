import feedparser
import requests
from feedgen.feed import FeedGenerator

# Usamos el RSS oficial de la playlist de YouTube
SOURCE_RSS = "https://www.youtube.com/feeds/videos.xml?playlist_id=PLTfCDg6nbbMs"

KEYWORDS = [
    "Olimpia",
    "olimpia",
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"[*] Conectando con la playlist de YouTube...")
try:
    response = requests.get(SOURCE_RSS, headers=headers, timeout=30)
    print(f"[*] Código de respuesta HTTP: {response.status_code}")
except Exception as e:
    print(f"[!] Error HTTP: {e}")
    exit(1)

feed = feedparser.parse(response.content)
print(f"[*] Total de entradas encontradas: {len(feed.entries)}")

# Configuramos el generador con los estándares que exige Feedly
fg = FeedGenerator()
fg.id("https://github.com/RssFeedly/Olimpia-goles")
fg.title("Olimpia Goles - RSS Filtrado")
fg.link(href="https://github.com/RssFeedly/Olimpia-goles", rel="self")
fg.description("Videos filtrados de Olimpia desde YouTube")

added_count = 0

for entry in feed.entries:
    title = entry.get("title", "").strip()
    link = entry.get("link", "")
    entry_id = entry.get("id", link)
    
    print(f" -> Evaluando: '{title}'")

    if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
        fe = fg.add_entry()
        fe.id(entry_id)
        fe.title(title)
        fe.link(href=link)

        if hasattr(entry, "published"):
            fe.pubDate(entry.published)

        if hasattr(entry, "summary"):
            fe.description(entry.summary)
            
        print(f"    [MATCH] ¡Añadido al feed!")
        added_count += 1

print(f"[*] Total de videos agregados: {added_count}")
# Generamos el RSS en formato limpio
fg.rss_file("feed.xml", pretty=True)
print("[*] Archivo feed.xml generado correctamente.")
