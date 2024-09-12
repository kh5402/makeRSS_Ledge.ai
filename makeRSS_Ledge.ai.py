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
    print("RSSフィード生成を開始🚀")

    # RSSフィードの初期化
    feed = Rss201rev2Feed(
        title="Ledge.ai 複数カテゴリ",
        link="https://ledge.ai",
        description="Ledge.aiの複数カテゴリの最新記事",
        language="ja",
        pretty=True
    )

    for getURL in urls:
        print(f"{getURL} にアクセスするよ🌐")
        try:
            # Pyppeteerでブラウザを開く
            print("ブラウザ起動中...")
            browser = await launch(
                executablePath='/usr/bin/chromium-browser',
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu'
                ]
            )
            print("ブラウザ開いた📂")

            # ブラウザの起動を待つ
            await asyncio.sleep(5)

            page = await browser.newPage()
            await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
            print(f"{getURL} ページに移動中...")
            await page.goto(getURL, timeout=30000)
            print("ページに移動した✈️")

            # ページのHTMLを取得
            print("HTML取得中...")
            html = await page.content()

            # BeautifulSoupで解析
            print("HTML解析中...")
            soup = BeautifulSoup(html, 'html.parser')

            # window.__NUXT__の内容を取得してJSONデータをPythonの辞書に変換
            print("JSONデータ取得中...")
            nuxt_data = json.loads(await page.evaluate('() => JSON.stringify(window.__NUXT__)'))
            print(f"JSONデータ取得（一部）：{str(nuxt_data)[:100]}... 📥")

            # "data"キーの中にある"articles"キーの"data"キーの値を取得
            print("記事データ取得中...")
            try:
                articles = nuxt_data["data"][f"/categories/{getURL.split('/')[-2]}"]["articles"]["data"]
            except KeyError as e:
                print(f"エラー: JSONデータにキー {e} が見つかりません。JSONデータの構造を確認してください。")
                print(f"getURL: {getURL}")
                print(f"nuxt_data['data'].keys(): {nuxt_data['data'].keys()}")
                continue  # 次のURLに進む

            if not articles:
                print("警告: 記事データが空やで❗️")
            else:
                print(f"取得した記事数：{len(articles)} 📚")

            # 12個のデータを取得
            print("記事データ処理中...")
            for article in articles[:12]:
                title = article['attributes']['title']
                date_str = article['attributes']['createdAt']
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                url = "https://ledge.ai/articles/" + article['attributes']['slug']
                description = re.sub(r'\[.*?\]\(.*?\)', '', article['attributes']['contents'][0]['content'])

                # XMLのエスケープ処理
                title = title.replace('&', '&').replace('<', '<').replace('>', '>').replace('"', '"').replace("'", ''')
                description = description.replace('&', '&').replace('<', '<').replace('>', '>').replace('"', '"').replace("'", ''')

                # アイテムをフィードに追加
                feed.add_item(
                    title=title,
                    link=url,
                    description=description,
                    pubdate=date_obj
                )
            print("RSSフィードにデータ追加した📝")

        except Exception as e:
            print(f"エラー: {e}")
            print(f"URL: {getURL} の処理中にエラーが発生しました。")
        finally:
            if 'browser' in locals():
                await browser.close()
                print("ブラウザを閉じた🚪")

    # RSSフィードをファイルに書き出し
    print("RSSフィード書き出し中...")
    with open('feed.xml', 'w') as f:
        feed.write(f, 'utf-8')

    print("複数カテゴリのRSSフィードが生成されました🎉")

# 非同期関数を実行
asyncio.run(main())
