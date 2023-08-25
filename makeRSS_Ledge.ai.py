from bs4 import BeautifulSoup
from feedgenerator import Rss201rev2Feed
import requests
import datetime

url = 'https://ledge.ai/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 新着記事の部分を取得
new_articles_section = soup.find_all('div', class_='flex flex-col gap-6')[1]

# 記事のタイトルとリンクを取得
articles = []
for article in new_articles_section.find_all('div', class_='flex flex-col gap-6'):
    title = article.text.strip()
    link = article.find('a')['href']
    articles.append((title, link))

feed = Rss201rev2Feed(
    title='Ledge.aiの最新記事',
    link=url,
    description='Ledge.aiの最新記事のRSSフィード',
)

# 各記事から詳細を取得
for title, link in articles:
    article_response = requests.get(link)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')

    # 説明
    description_tag = article_soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else "説明が見つかりません"

    # 日付
    date_tag = article_soup.find('meta', attrs={'property': 'article:published_time'})
    date = datetime.datetime.fromisoformat(date_tag['content']) if date_tag else "日付が見つかりません"

    # RSSエントリーに記事情報を追加
    feed.add_item(
        title=title,
        link=link,
        description=description,
        pubdate=date
    )

# RSSファイルに保存
with open('feed.xml', 'w', encoding='utf-8') as file:
    feed.write(file, 'utf-8')

print(f"合計 {len(articles)} 記事を取得し、RSSファイルに保存しました。")
