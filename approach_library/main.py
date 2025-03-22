# Importing Libraries and functions from utils.py
import time
from utils.news_extraction import extract_news
from utils.news_summarisation import summarize_text
from utils.news_sentiment import analyze_sentiment
from utils.topic_extraction import preprocess_text, train_lda, extract_topic_words
from utils.comparative_analysis import comparative_sentiment_analysis
from utils.text_to_speech import text_to_speech 

def analyze_company_news(company):
    # Extract news articles
    start_time = time.time()
    articles = extract_news(company)
    extraction_time = time.time() - start_time

    if not articles:
        return {"message": "No news articles found. Try a different company."}

    articles_data = []  # List to store processed articles

    # Extract texts from articles for sentiment analysis
    texts = [article["text"] for article in articles]

    # Perform sentiment analysis
    start_time = time.time()
    sentiment_results = analyze_sentiment(texts)
    sentiment_time = time.time() - start_time

    # Process each article
    for i, (article, sentiment) in enumerate(zip(articles, sentiment_results["Predicted Sentiment"]), start=1):
        start_time = time.time()
        summary = summarize_text(article["text"])  # Summarize article
        summarization_time = time.time() - start_time

        # Extract topics for the specific article
        preprocessed_text = preprocess_text([article["text"]])
        lda_model, dictionary = train_lda(preprocessed_text)
        topic_words = extract_topic_words(lda_model)

        article_entry = {
            "Title": article["title"],
            "Summary": summary,
            "Sentiment": sentiment,
            "Topics": topic_words
        }
        articles_data.append(article_entry)

    # Perform comparative sentiment analysis
    analysis_result = comparative_sentiment_analysis(company, articles_data)

    # Generate a summary speech for the entire report
    final_summary = f"{company}’s latest news coverage is mostly {analysis_result['Final Sentiment Analysis']}."
    audio_file = text_to_speech(final_summary)  # Generate TTS

    # Construct final JSON output
    output = {
        "Company": company,
        "Articles": articles_data,
        "Comparative Sentiment Score": analysis_result,
        "Audio": f"[Play {audio_file}]"  #  Include a playable reference
    }

    return output
