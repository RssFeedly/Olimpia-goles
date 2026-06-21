import feedparser
import requests
from feedgen.feed import FeedGenerator

SOURCE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCDnZ8zbVWLaVfuDmNuWq7rw"

KEYWORDS = [
    "Olimpia",
    
]

rss_text = requests.get(SOURCE_RSS, timeout=30).text
feed = feedparser.parse(rss_text)

fg = FeedGenerator()
fg.title("RSS Filtrado")
fg.link(href=SOURCE_RSS)
fg.description("Videos filtrados de YouTube")

for entry in feed.entries:
    title = entry.title

    if any(k.lower() in title.lower() for k in KEYWORDS):
        fe = fg.add_entry()

        fe.title(title)
        fe.link(href=entry.link)

        if hasattr(entry, "published"):
            fe.pubDate(entry.published)

        if hasattr(entry, "summary"):
            fe.description(entry.summary)

fg.rss_file("feed.xml")
