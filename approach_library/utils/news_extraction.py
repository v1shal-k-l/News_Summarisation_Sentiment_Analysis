# Importing Libraries
import nest_asyncio
from typing import List, Dict
from duckduckgo_search import DDGS
from phi.tools.newspaper4k import Newspaper4k
import time

nest_asyncio.apply()

def extract_news(article_topic: str, num_search_results: int = 15, max_retries: int = 3) -> List[Dict[str, str]]:
    """
    Extracts full news articles based on the given topic and number of search results.

    Args:
        article_topic: The topic to search for.
        num_search_results: The number of search results to retrieve.
        max_retries: The maximum number of retries if an article fails to scrape.

    Returns:
        A list of dictionaries, where each dictionary represents a news article.
    """
    news_results = []
    ddgs = DDGS()
    newspaper_tools = Newspaper4k()
    
    results = ddgs.news(keywords=article_topic, max_results=num_search_results*15)  
    
    for r in results:
        if "url" in r:
            retries = 0
            while retries < max_retries:
                try:
                    article_data = newspaper_tools.get_article_data(r["url"])
                    
                    if article_data and "text" in article_data and len(article_data["text"]) > 100:
                        news_results.append({
                            "title": r.get("title", "No Title"),
                            "text": article_data["text"]  
                        })
                        break 
                    else:
                        retries += 1
                        time.sleep(1)  
                except Exception as e:
                    retries += 1
                    time.sleep(1)
                    
        # Stop if we have collected enough articles
        if len(news_results) >= num_search_results:
            break
    
    return news_results
