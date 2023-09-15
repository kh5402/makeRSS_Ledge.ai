from bs4 import BeautifulSoup
from feedgenerator import Rss201rev2Feed
from datetime import datetime
import asyncio
import json
import re
from pyppeteer import launch

# 複数のURLをリストで用意
urls = [
    'https://ledge.ai/categories/business/',
    'https://ledge.ai/categories/learning/', 
    'https://ledge.ai/categories/engineering/',
    'https://ledge.ai/categories/academic/',
    'https://ledge.ai/categories/public/',
    'https://ledge.ai/categories/entertainment/'
]

async def main():

    # RSSフィードの初期化はループの外で行う
    feed = Rss201rev2Feed(
        title="Ledge.ai 複数カテゴリ",
        link="https://ledge.ai",
        description="Ledge.aiの複数カテゴリの最新記事",
        language="ja",
        pretty=True
    )
    
    for getURL in urls:

        # Pyppeteerでブラウザを開く
        browser = await launch(
            executablePath='/usr/bin/chromium-browser',
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu'
            ],
        )

        page = await browser.newPage()
        await page.goto(getURL)

        # ページのHTMLを取得
        html = await page.content()

        # BeautifulSoupで解析
        soup = BeautifulSoup(html, 'html.parser')

        # window.__NUXT__の内容を取得してJSONデータをPythonの辞書に変換
        nuxt_data = json.loads(await page.evaluate('() => JSON.stringify(window.__NUXT__)'))

        # "data"キーの中にある"articles"キーの"data"キーの値を取得
        articles = nuxt_data["data"][f"/categories/{getURL.split('/')[-2]}"]["articles"]["data"]

        # 12個のデータを取得 ➡ 1ページに12個の記事あるから。
        for article in articles[:12]:
            title = article['attributes']['title']
            date_str = article['attributes']['createdAt']
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            date_formatted = date_obj.strftime("%Y/%m/%d %H:%M")
            url = "https://ledge.ai/articles/" + article['attributes']['slug']
            description = re.sub(r'\[.*?\]\(.*?\)', '', article['attributes']['contents'][0]['content'])

            # アイテムをフィードに追加
            feed.add_item(
                title=title,
                link=url,
                description=description,
                pubdate=date_obj
            )

    # RSSフィードをファイルに書き出し
    with open('feed_multi_categories.xml', 'w') as f:
        feed.write(f, 'utf-8')

    print("複数カテゴリのRSSフィードが生成されました🎉")

# 非同期関数を実行
asyncio.get_event_loop().run_until_complete(main())
