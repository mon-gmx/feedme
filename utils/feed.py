import feedparser
import logging
from uuid import uuid4


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
        feed_entries = getattr(feed, "entries", [])
        if len(feed_entries) > 10:
            feed_entries = feed_entries[-10:]
        for entry in feed_entries[::-1]:
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
            f"<div class=\"container-lg\" align=\"right\">"
            f"<h2>{feed_dict['title']}\n"
            f"<a href=\"{feed_dict['url']}\">&#x1F517;</a>\n</h2>\n"
            f"<h3>Description: {feed_dict['subtitle']}</h3>\n"
            f"<i>{feed_dict['summary']}</i><br/>"
            f"</div>"
        )

        accordion_id = str(uuid4())
        markdown_entry += f"<div id=\"accordion_{accordion_id}\" role=\"tablist\">\n"
        for entry in enumerate(feed_dict["entries"]):
            markdown_entry += f"<div class=\"card\">"
            markdown_entry += f"<div class=\"card-header\" id=\"heading_{entry[0]}\">"
            markdown_entry += f"<h2 class=\"mb-0\">"
            markdown_entry += (
                f"<button class=\"btn text-left font-weight-bold\" type=\"button\" data-toggle=\"collapse\" "
                f"data-target=\"#panel_{entry[0]}\" data-parent=\"#accordion_{accordion_id}\">\n"
            )
            markdown_entry += f"{entry[1]['title']}<a href=\"{entry[1]['url']}\">&#x1F517;</a><br/>\n"
            markdown_entry += f"<i>{entry[1]['date']}</i>\n"
            markdown_entry += f"</button>\n</h2>\n</div>\n\n"
            markdown_entry += f"<div id=\"panel_{entry[0]}\" class=\"collapse\">\n"
            markdown_entry +=f"<div class=\"card-body\">"
            markdown_entry +=f"{entry[1]['summary']}\n"
            markdown_entry += "</div>\n</div><br/>\n"
        markdown_entry += "</div>\n"
    return markdown_entry
