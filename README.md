# FEEDME
---

I built this silly project not only to work with some libraries for RSS feed, but to actually do something about the uglyness of relying on social media to learn about things that I care.

This project is not meant to serve the public, it might as well just be a script for me or someone else, but I think this is good to hook as a service into a raspberry and have a feed available on demand.

To run this project all that's needed is to execute FastAPI and call the only endpoint available: `/feeds`.

### How to turn this into a service within your raspberry?

The following instructions may be flawed in all security and reliability aspects, mind that this runs in a raspberry next to my computer, thus, I could really care less about access to the board or failure.

```
[Unit]
Description=RSS feed loading

[Service]
User=rssfeed
Group=rssfeed
Type=simple
WorkingDirectory=/mnt/rssfeed/feedme
Environment="PATH=/mnt/rssfeed/feedme/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/bin/bash -c 'source /mnt/rssfeed/feedme/venv/bin/activate; \
    /mnt/rssfeed/feedme/venv/bin/fastapi run --port 8899'
Restart=always
RestartSec=30s

[Install]
WantedBy=multi-user.target
```
