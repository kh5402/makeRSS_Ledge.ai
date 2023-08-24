import requests
from bs4 import BeautifulSoup
import feedparser

url = 'https://ledge.ai/'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 記事へのリンクを取得
article_links = [a['href'] for a in soup.find_all('a', href=True) if '/articles/' in a['href']]

# 重複を取り除く
article_links = list(set(article_links))

print(article_links)

# RSSフィードを作成
feed = feedparser.FeedParserDict()
feed['feed'] = {'title': 'Ledge.aiの最新記事', 'link': url, 'description': 'Ledge.aiの最新記事のRSSフィード'}
feed['entries'] = []

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
    entry = {
        'title': title,
        'link': link,
        'description': description,
        'published': date
    }
    feed['entries'].append(entry)

# RSSファイルに保存
with open('feed.xml', 'w', encoding='utf-8') as file:
    file.write(feedparser.dumps(feed))

print(f"合計 {len(article_links)} 記事を取得し、RSSファイルに保存しました。")
