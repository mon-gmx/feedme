import logging
import random
from uuid import uuid4

import feedparser
import requests

log = logging.getLogger(__name__)

def feed_to_dict(feed_url: str, limit: int = 10) -> dict:
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
        if len(feed_entries) > limit:
            feed_entries = feed_entries[-limit:]
        for entry in feed_entries[::-1]:
            if getattr(entry, "summary"):
                feed_dict["entries"].append(
                    {
                        "title": getattr(entry, "title", "Untitled"),
                        "url": getattr(entry, "link", "No link"),
                        "date": getattr(entry, "published", "Unknown date"),
                        "summary": getattr(entry, "summary", None),
                    }
                )
    return feed_dict


def dict_to_markdown(feed_dict: dict) -> str:
    markdown_entry = ""

    if feed_dict:
        if not feed_dict.get("entries", []):
            return ""
        markdown_entry = (
            f'<div class="container-lg" align="right">\n'
            f"  <h2>{feed_dict['title']}\n"
            f"  <a href=\"{feed_dict['url']}\">&#x1F517;</a>\n</h2>\n"
            f"  <h3>Description: {feed_dict['subtitle']}</h3>\n"
            f"  <i>{feed_dict['summary']}</i><br/>\n"
            f"</div>\n"  # container for feed
        )

        accordion_id = str(uuid4())
        markdown_entry += f'<div id="accordion_{accordion_id}" role="tablist">\n'
        for entry in enumerate(feed_dict["entries"]):
            if not entry:
                continue
            markdown_entry += f'  <div class="card">\n'
            markdown_entry += f'    <div class="card-header" id="heading_{entry[0]}">\n'
            markdown_entry += f'      <h2 class="mb-0">\n'
            markdown_entry += (
                f'        <button class="btn text-left font-weight-bold" type="button" data-toggle="collapse" '
                f'data-target="#panel_{entry[0]}" data-parent="#accordion_{accordion_id}">\n'
            )
            markdown_entry += f"        {entry[1]['title']}<a href=\"{entry[1]['url']}\">&#x1F517;</a><br/>\n"
            markdown_entry += f"          <i>{entry[1]['date']}</i>\n"
            markdown_entry += f"        </button>\n"
            markdown_entry += f"      </h2>\n"
            markdown_entry += f"    </div>\n"  # card header
            markdown_entry += f'    <div id="panel_{entry[0]}" class="collapse">\n'
            markdown_entry += f'      <div class="card-body">\n'
            markdown_entry += f"        {entry[1]['summary']}\n"
            markdown_entry += f"      </div>\n"  # card body
            markdown_entry += f"    </div>\n"  # panel
            markdown_entry += f"  </div>\n"  # card
    markdown_entry += f"</div>\n"
    return markdown_entry


def get_random_image(images_src_url: str) -> str:
    image_html = ""
    image_src = {}
    try:
        image_src = requests.get(images_src_url).json()
    except requests.HTTPError:
        log.error("Failed to pull image from url")

    try:
        images = image_src.get("data", {}).get("children", [])
        if images:
            random_url = (
                images[random.randint(0, len(images))].get("data", {}).get("url", "")
            )
            if random_url:
                image_html = f"<img src=\"{ random_url }\" class=\"img-fluid max-width: 40%; and height: auto;\"></img>"
            else:
                log.warning(f"Could not fetch the image from the list: {random_url}")
        else:
            log.warning(f"Images request retrieved no data: {images}")
    except KeyError:
        log.error("The response came in an unexpected format")
    return image_html
