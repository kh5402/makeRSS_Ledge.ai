from bs4 import BeautifulSoup
from feedgenerator import Rss201rev2Feed
import requests
import datetime
import asyncio
import json
from pyppeteer import launch

getURL = 'https://ledge.ai/categories/business/'

async def main():

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
    articles = nuxt_data["data"]["/categories/business"]["articles"]["data"]

    # 12個のデータを取得 ➡ 1ページに12個の記事あるから。
    for article in articles[:12]:
        print(article)  # ここで各記事のデータをプリント
    
# 非同期関数を実行
asyncio.get_event_loop().run_until_complete(main())
