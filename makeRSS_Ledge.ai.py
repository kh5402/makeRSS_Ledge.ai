from bs4 import BeautifulSoup
from feedgenerator import Rss201rev2Feed
import requests

# URL
url = 'https://ledge.ai/'

# URLからHTMLを取得
response = requests.get(url)
html_content = response.text

# BeautifulSoupで解析
soup = BeautifulSoup(html_content, 'html.parser')
print(soup)

# RSSフィードを生成
feed = Rss201rev2Feed(
    title="Ledge.ai Articles",
    link=url,
    description="Latest articles from Ledge.ai",
)

# 記事のタイトルとURLを取得してフィードに追加
for article in soup.select('article'):
    title = article.select_one('h2').text if article.select_one('h2') else None
    url = article.select_one('a')['href'] if article.select_one('a') else None
    feed.add_item(title=title, link=url)

# RSSフィードをXMLファイルとして保存
with open('feed.xml', 'w', encoding='utf-8') as file:
    feed.write(file, 'utf-8')

print("RSS feed generated successfully!")
