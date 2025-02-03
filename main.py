import logging
from datetime import UTC, datetime, timedelta
from functools import lru_cache, wraps

import markdown
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

import config
from utils import feed

app = FastAPI()
log = logging.getLogger(__name__)


def ttl_lru_cache(ttl: int = 1800, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.ttl = timedelta(seconds=ttl)
        func.expiry = datetime.now(UTC) + func.ttl

        @wraps(func)
        # wrapper function to clear cache after expiration
        def wrapped_func(*args, **kwargs):
            if datetime.now(UTC) > func.expiry:
                func.cache_clear()
                func.expiration = datetime.now(UTC) + func.ttl
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


@ttl_lru_cache(ttl=config.cache_ttl, maxsize=None)
def load_cached_feed(feed_url):
    return feed.feed_to_dict(feed_url=feed_url, limit=config.feed_limit)


def compose_feed():
    html = config.html_head
    image_header = feed.get_random_image(config.images_src_url)
    if image_header:
        html += f"\n<div class=\"container\" align=\"center\">\n"
        html += f"  {image_header}\n"
        html += f"</div>\n"
    composed_feed = ""
    for item in config.feeds:
        feed_url, is_cached = item
        if is_cached:
            composed_feed += feed.dict_to_markdown(
                load_cached_feed(feed_url)
            )
        else:
            composed_feed += feed.dict_to_markdown(
                feed.feed_to_dict(feed_url=feed_url, limit=config.feed_limit)
            )
    if composed_feed:
        try:
            html += markdown.markdown(composed_feed)
        except Exception as error:
            log.error(f"Failed to parse markdown into HTML, {error}")
    return html


@app.get("/feeds")
async def serve_feed(request: Request = None):
    if request.method == "GET":
        response = HTMLResponse(content=compose_feed(), status_code=200)
        response.headers.update(config.headers)
        return response
    raise HTTPException(status_code=400, detail="Invalid method")
