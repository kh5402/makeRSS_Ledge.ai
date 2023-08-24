import re
from datetime import datetime
import requests
import feedgenerator

def create_rss_feed(url):
    # URLからHTMLを取得
    response = requests.get(url)
    text = response.text

    # 記事ごとにデータを分割
    articles_data = text.split('slug:"')[1:]

    # RSSフィードを生成
    feed = feedgenerator.Rss201rev2Feed(
        title="Ledge.ai Articles",
        link=url,
        description="Latest articles from Ledge.ai",
    )

    for article_data in articles_data:
        # スラグを抽出
        slug_pattern = re.compile(r'(.*?)"')
        slug = slug_pattern.search(article_data).group(1)

        # 日付を抽出
        date_pattern = re.compile(r'scheduled_at:"(.*?)"')
        date_str = date_pattern.search(article_data).group(1)
        date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

        # コンテンツを抽出
        content_pattern = re.compile(r'content:"(.*?)"')
        content = content_pattern.search(article_data).group(1)

        # URLを構築
        article_url = "https://ledge.ai/articles/" + slug

        feed.add_item(
            title=article_url,  # タイトルとしてURLを使用
            link=article_url,
            pubdate=date,
            description=content,
        )

    # RSSフィードを文字列として返す
    return feed.writeString('utf-8')

# URL
url = 'https://ledge.ai/'

# RSSフィードを生成
rss_feed_content = create_rss_feed(url)

# フィードをファイルとして保存
output_file_path = 'feed.xml'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(rss_feed_content)

print("RSS feed generated successfully!")
