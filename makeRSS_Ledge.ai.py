from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET

url = 'https://ledge.ai/'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# XMLのルートを作成
root = ET.Element("articles")

# 記事へのリンクを取得
article_links = [a['href'] for a in soup.find_all('a', href=True) if '/articles/' in a['href']]

# 重複を取り除く
article_links = list(set(article_links))

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

    # XMLに記事情報を追加
    article_elem = ET.SubElement(root, "article")
    ET.SubElement(article_elem, "title").text = title
    ET.SubElement(article_elem, "description").text = description
    ET.SubElement(article_elem, "url").text = link
    ET.SubElement(article_elem, "date").text = date

# XMLをファイルに保存
tree = ET.ElementTree(root)
tree.write("feed.xml")

print(f"合計 {len(article_links)} 記事を取得し、XMLファイルに保存しました。")
