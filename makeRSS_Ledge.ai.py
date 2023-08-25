import requests
from bs4 import BeautifulSoup
from feedgenerator import Rss201rev2Feed

url = 'https://ledge.ai/'

# RSSフィードを作成
feed = Rss201rev2Feed(
    title='Ledge.aiの最新記事',
    link=url,
    description='Ledge.aiの最新記事のRSSフィード'
)

# 各記事から詳細を取得
for link in article_links:
    article_response = requests.get(link)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')

    # タイトル
    title = article_soup.find('title').text

    # 説明
    description_tag = article_soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else "説明が見つかりません"

    # 日付
    date_tag = article_soup.find('meta', attrs={'property': 'article:published_time'})
    date = date_tag['content'] if date_tag else "日付が見つかりません"

    # RSSエントリーに記事情報を追加
    feed.add_item(
        title=title,
        link=link,
        description=description,
        pubdate=date
    )

# RSSファイルに保存
with open('feed.xml', 'w', encoding='utf-8') as file:
    feed.write(file)

print(f"合計 {len(article_links)} 記事を取得し、RSSファイルに保存しました。")
