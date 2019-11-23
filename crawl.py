from facebook_scraper import get_posts
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString
import re
import json

import pymysql
from time import sleep
sleep(0.05)
conn = pymysql.connect(host='localhost', user='root', password='Your Password Goes Here',
                       db='wikirecent', charset='utf8')


json_output = []
cnt = 0

for post in get_posts('wikitree.page', pages=100000000):
    try:
        sleep(0)
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


        try:
            curs = conn.cursor()
            # SQL문 실행
            sql = f"INSERT INTO `data` (`id`, `title`, `body`, `lead_paragraphs`, `time`, `link`, `fb_post`) VALUES (NULL, '{pymysql.escape_string(title)}', '{pymysql.escape_string(body)}', '{json.dumps(lead_paragraphs, ensure_ascii=False)}', '{pymysql.escape_string(time)}', '{pymysql.escape_string(post['link'])}', '{pymysql.escape_string(text)}');"
            print(sql)
            curs.execute(sql)
            conn.commit()
        except:
            pass

        cnt+=1
        print("Crawled!"+post['link'])
    except:
        pass

f = open("result.json", 'w')
f.write(json.dumps(json_output,  ensure_ascii = False))
f.close()


#print(json.dumps(json_output,  ensure_ascii = False))