import feedparser

def parse_feed_info(url, item_limit=5):
    feed = feedparser.parse(url)
    items = []
    for item in feed['items']:
        try:
            items.append(dict(
                title = item['title'],
                url = item['links'][0]['href']
                ))
        except KeyError:
            pass

    return items[:item_limit]

def get_feed_elements(feeds, item_limit = 5):
        items = []
        for name, url in feeds.items():
            items.append(dict(title = name, url = ''))
            items.extend(parse_feed_info(url, item_limit))

        return dict(feeds = items)


    

