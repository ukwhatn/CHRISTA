import json
import logging
import time

import mysql.connector
import requests
from bs4 import BeautifulSoup

import wikidot

GASURL = "https://script.google.com/macros/s/AKfycbzfJN5vw8goZdQjHbh9GfVOjM877D1Zc0JG2s31HZCway6SJu5iMpS4WZWLAKbJsXEeJQ/exec"

interval = 600

mysql_config = {
    "host": "db",
    "port": "3306",
    "user": "application",
    "password": "applicationpassword",
    "database": "Master",
    "charset": "utf8mb4",
    "collation": "utf8mb4_general_ci",
    "autocommit": False
}

# DBコンテナの起動を待つ
while True:
    try:
        with mysql.connector.Connect(**mysql_config) as connect:
            logging.info("connected")
        break
    except mysql.connector.errors.InterfaceError as e:
        logging.warning("waiting database.....")
        time.sleep(3)
        continue

while True:
    try:
        # Wikidotクライアント作成
        wikidot_client = wikidot.Client()
        # 既知ページ取得
        # FIXME:
        #   fullname被りを考慮せよ
        with mysql.connector.Connect(**mysql_config) as connect:
            with connect.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM drafts")
                known_drafts = cursor.fetchall()
                known_drafts_fullname = [draft["fullname"] for draft in known_drafts]

        # bs4パース
        listpages = requests.get(
            "http://scp-jp-sandbox3.wikidot.com/draft:3396310-216-356c/lp_category/draft/lp_tags/%2B_criticism-in%20%2B_contest/lp_order/updated_at%20desc/lp_limit/999999/lp_perPage/250/lp_p/1/#u-hanyoulp")
        soup = BeautifulSoup(listpages.content, "lxml")

        # エレメントごとにデータ取得
        page_datas = []
        pages = soup.find_all("div", class_="list-pages-item")
        for page in pages:
            if page.find("span", class_="lp_title") is None:
                continue
            title = page.find("span", class_="lp_title").text
            fullname = page.find("span", class_="lp_fullname").text
            author = wikidot.Parser.printUser(wikidot_client, page.find("span", class_="lp_created_by").find("span", class_="printuser", recursive=False))
            hidden_tags = page.find("span", class_="lp_hiddentags").text.split(" ")
            if "_scp-jp" in hidden_tags:
                category = "SCP-JP"
            elif "_tale_jp" in hidden_tags:
                category = "Tale-JP"
            elif "_goi-format-jp" in hidden_tags:
                category = "GoIF-JP"
            else:
                category = "unknown"
            if fullname not in known_drafts_fullname:
                page_datas.append([fullname, title, author.id, author.unixName, category])
        with mysql.connector.Connect(**mysql_config) as connect:
            with connect.cursor() as cursor:
                for page in page_datas:
                    logging.warning("Find new draft: " + page[0])
                    cursor.execute("INSERT IGNORE INTO drafts (fullname, title, author_id, author_name, category) VALUES (%s, %s, %s, %s, %s)",
                                   tuple(page))
                    r = requests.post(
                        url=GASURL,
                        data=json.dumps({
                            "url": "http://scp-jp-sandbox3.wikidot.com" + page[0],
                            "title": page[1],
                            "author": {
                                "id": page[2],
                                "name": page[3]
                            },
                            "category": page[4]
                        }),
                        headers={"Content-Type": "application/json"}
                    )
            connect.commit()

    except Exception as e:
        logging.error(e)
        pass

    time.sleep(interval)
