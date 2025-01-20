import logging
import config
import markdown

from utils import feed
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from functools import lru_cache

app = FastAPI()
log = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def compose_feed():
    html = config.html_head
    composed_feed = ""
    for feed_url in config.feeds:
        composed_feed += feed.dict_to_markdown(feed.feed_to_dict(feed_url=feed_url, limit=config.feed_limit))
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
