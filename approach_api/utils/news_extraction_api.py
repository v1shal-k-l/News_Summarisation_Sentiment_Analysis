# Importing Libraries
import requests
from bs4 import BeautifulSoup
import os

# NewsAPI Key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def extract_news(company, num_articles=15):
    """Fetch multiple news articles from NewsAPI and return titles and contents."""
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={NEWS_API_KEY}&language=en&pageSize={num_articles}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return []

    data = response.json()
    articles = data.get("articles", [])

    if not articles:
        print("No articles found.")
        return []

    extracted_articles = []

    for article in articles[:num_articles]: 
        article_url = article.get("url", "No URL available.")

        # Scraping the article for title and content
        article_response = requests.get(article_url)
        if article_response.status_code == 200:
            soup = BeautifulSoup(article_response.content, 'html.parser')
            title = soup.title.string if soup.title else "No Title Found"
            
            # Extracting content and cleaning it
            paragraphs = soup.find_all('p')
            content = ' '.join(p.get_text().strip() for p in paragraphs if p.get_text().strip())

            # Optionally, filtering out unwanted text patterns
            unwanted_patterns = ["Want to read", "Nickname:", "Password:", "The Fine Print:"]
            for pattern in unwanted_patterns:
                content = content.replace(pattern, "")
            
            # Cleaning up extra spaces
            content = ' '.join(content.split())

            extracted_articles.append({"title": title, "content": content})

    return extracted_articles

