from bs4 import BeautifulSoup
from feedgenerator import Rss201rev2Feed
import requests
import datetime
import asyncio
from pyppeteer import launch

getURL = 'https://ledge.ai/'

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

    print(soup)

    
    # window.__NUXT__の内容を取得
    nuxt_data = await page.evaluate('() => window.__NUXT__')
    print(nuxt_data)
    
# 非同期関数を実行
asyncio.get_event_loop().run_until_complete(main())
