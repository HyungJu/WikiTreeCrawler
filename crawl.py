from facebook_scraper import get_posts
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString
import re
import json
for post in get_posts('wikitree.page', pages=5):
    text = post['post_text']

    html = urlopen(post['link'])
    bs = BeautifulSoup(html, "html.parser")
    #print(bs.find(class_='article_title').text)
    contents = bs.find(id='wikicon')

    lead_paragraphs_bs = contents.find(id='lead_paragraph')
    lead_paragraphs_bs = lead_paragraphs_bs.findAll('li')

    lead_paragraphs = []
    for lead_paragraph in lead_paragraphs_bs:
        l = re.sub("\r|\n|•", "", lead_paragraph.text)
        lead_paragraphs.append(l.strip())



    body = ""
    contents = bs.select('#wikicon > div', recrusive=True, class_='')
    for content in contents:
        if content.string is not None:
            body+=content.string
            body+="\n"


    title = bs.find(class_="article_title").text

    time = bs.select(".article_byline > .time")[0].string


    data = {"title": title, "body": body, "lead_paragraphs": lead_paragraphs, "time": time, "link": post['link'], "fb_post": text}

    print(json.dumps(data,  ensure_ascii = False))