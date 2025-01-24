feed_limit = 30

cache_ttl = 8 * 3600  # 8 hours

feeds = [
    "https://www.howtogeek.com/feed/",
    "https://news.ycombinator.com/rss",
    "https://realpython.com/atom.xml?format=xml",
    "https://www.cyberciti.com/feed/",
    "https://feeds.feedburner.com/PythonSoftwareFoundationNews",
    "https://www.linuxjournal.com/node/feed",
    "https://go.dev/blog/feed.atom?format=xml",
    "https://blog.bytebytego.com/feed",
]

headers = {
    "Cache-Control": "max-age=864000"
}

html_head = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.bundle.min.js"></script>
</head>
"""
