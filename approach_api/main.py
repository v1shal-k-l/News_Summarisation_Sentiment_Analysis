# Importing Libraries and functions from utils.py
import json
from utils.news_extraction_api import extract_news
from utils.news_summarisation import summarize_text
from utils.news_sentiment import analyze_sentiment
from utils.topic_extraction import preprocess_text, train_lda, extract_topic_words
from utils.comparative_analysis import comparative_sentiment_analysis
from utils.text_to_speech import text_to_speech  

# Function
def analyze_company_news(company):
    # Extracting articles
    articles = extract_news(company)

    if not articles:
        return {"message": "No news articles found. Try a different company."}

    articles_data = []  

    # Extracting content from articles
    texts = [article["content"] for article in articles]

    # Sentiment analysis
    sentiment_results = analyze_sentiment(texts)

    # Process each article
    for i, (article, sentiment) in enumerate(zip(articles, sentiment_results["Predicted Sentiment"]), start=1):
        summary = summarize_text(article["content"])  # Summarize article

        # Extract topics for the each article
        preprocessed_text = preprocess_text([article["content"]])
        lda_model, dictionary = train_lda(preprocessed_text)
        topic_words = extract_topic_words(lda_model)

        article_entry = {
            "Title": article["title"],
            "Summary": summary,
            "Sentiment": sentiment,
            "Topics": topic_words
        }
        articles_data.append(article_entry)

    # Performing comparative sentiment analysis
    analysis_result = comparative_sentiment_analysis(company, articles_data)

    # Generating a final summary for the entire task
    final_summary = f"{company}’s latest news coverage is mostly {analysis_result['Final Sentiment Analysis']}."
    audio_file = text_to_speech(final_summary)  # Generate TTS

    
    output = {
        "Company": company,
        "Articles": articles_data,
        "Comparative Sentiment Score": analysis_result,
        "Audio": f"[Play {audio_file}]"  
    }

    return output

if __name__ == "__main__":
    company = input("Enter the company name for analysis: ").strip()
    result = analyze_company_news(company)
    print(json.dumps(result, indent=4, ensure_ascii=False))