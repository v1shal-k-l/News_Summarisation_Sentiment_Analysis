# Importing Libraries
from collections import Counter

# Function
def comparative_sentiment_analysis(company, articles, max_comparisons=10, chunk_size=5):
    """
    Perform a comparative sentiment analysis on multiple articles.
    """
    overall_sentiment_counts = Counter()
    overall_coverage_differences = []
    all_topics = []

    if not articles:
        print("No articles found for analysis.")
        return {
            "Company": company,
            "Articles": [],
            "Comparative Sentiment Score": {
                "Sentiment Distribution": {},
                "Coverage Differences": [],
                "Topic Overlap": {"Common Topics": [], "Unique Topics Per Article": []}
            },
            "Final Sentiment Analysis": "No data available."
        }

    # Process articles in chunks
    for start in range(0, len(articles), chunk_size):
        chunk = articles[start:start + chunk_size]

        # Count sentiment distribution
        sentiment_counts = Counter(article["Sentiment"] for article in chunk)
        overall_sentiment_counts.update(sentiment_counts)

        # Identify coverage differences
        for i in range(len(chunk) - 1):
            for j in range(i + 1, len(chunk)):
                if len(overall_coverage_differences) >= max_comparisons:
                    break
                article1, article2 = chunk[i], chunk[j]
                comparison = {
                    "Comparison": f"'{article1.get('Title', 'Article 1')}' vs '{article2.get('Title', 'Article 2')}'",
                    "Impact": f"{article1.get('Topics', [])} vs {article2.get('Topics', [])}"
                }
                overall_coverage_differences.append(comparison)

        # Extract topics ensuring valid lists
        topics = [set(article.get("Topics", [])) for article in chunk if isinstance(article.get("Topics", list), list) and article.get("Topics", [])]
        all_topics.extend(topics)

    # Determine common and unique topics
    if len(all_topics) == 0:
        common_topics = set()  # No topics found
    elif len(all_topics) == 1:
        common_topics = all_topics[0]  # Only one article, take its topics as common
    else:
        common_topics = set.intersection(*all_topics) 

    unique_topics = [{"Article": i + 1, "Unique Topics": list(topics - common_topics)}
                     for i, topics in enumerate(all_topics)]

    common_topics = list(common_topics)

    # Final sentiment summary
    final_analysis = "The news coverage is mostly "
    if overall_sentiment_counts["Positive"] > overall_sentiment_counts["Negative"]:
        final_analysis += "positive, indicating potential growth."
    elif overall_sentiment_counts["Negative"] > overall_sentiment_counts["Positive"]:
        final_analysis += "negative, suggesting challenges ahead."
    else:
        final_analysis += "balanced, with mixed reactions."

    # Final JSON structure
    return {
        "Comparative Sentiment Score": {
            "Sentiment Distribution": dict(overall_sentiment_counts),
            "Coverage Differences": overall_coverage_differences,
            "Topic Overlap": {
                "Common Topics": common_topics,
                "Unique Topics Per Article": unique_topics
            }
        },
        "Final Sentiment Analysis": final_analysis
    }
