import feedparser
import logging


log = logging.getLogger(__name__)


def feed_to_dict(feed_url: str) -> dict:
    feed_dict = {}
    try:
        feed = feedparser.parse(feed_url)
    except (
        Exception
    ) as error:  # seems there is no specific exception from the parser itself
        log.error(f"Failed to read the URL, {error}")
    if getattr(feed, "feed") and getattr(feed, "entries"):
        feed_dict = {
            "url": feed_url,
            "title": getattr(feed.feed, "title", "Untitled feed"),
            "subtitle": getattr(feed.feed, "subtitle", "No description"),
            "summary": getattr(feed, "summary", "No summary"),
            "entries": [],
        }
        for entry in getattr(feed, "entries", []):
            if getattr(entry, "summary"):
                feed_dict["entries"].append(
                    {
                        "title": getattr(entry, "title", "Untitled"),
                        "url": getattr(entry, "link", "No link"),
                        "date": getattr(entry, "published", "Unknown date"),
                        "summary": entry.summary,
                    }
                )
    return feed_dict


def dict_to_markdown(feed_dict: dict) -> str:
    markdown_entry = ""

    if feed_dict:
        markdown_entry = (
            f"---\n"
            f"## {feed_dict['title']} ({feed_dict['url']})\n\n"
            f"### Description: {feed_dict['subtitle']}\n\n"
            f"**Summary: {feed_dict['summary']}**\n\n\n"
        )

        for entry in feed_dict["entries"]:
            if entry["url"]:
                markdown_entry += f"#### [{entry['title']}]({entry['url']})\n"
            else:
                markdown_entry += f"#### entry['title']\n"
            markdown_entry += f"**{entry['date']}**\n" f"{entry['summary']}\n\n\n"

    return markdown_entry
