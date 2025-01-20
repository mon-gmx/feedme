feed_limit = 30

feeds = [
    "https://pycon.blogspot.com/feeds/posts/default",
    "https://realpython.com/atom.xml?format=xml",
    "https://news.ycombinator.com/rss",
    "https://explaining.software/rss",
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
