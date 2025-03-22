# Importing Libraries and functions from utils.py in approach_api
import streamlit as st
from approach_library.utils.news_extraction import extract_news
from approach_library.utils.news_summarisation import summarize_text
from approach_library.utils.news_sentiment import analyze_sentiment
from approach_library.utils.topic_extraction import preprocess_text, train_lda, extract_topic_words
from approach_library.utils.comparative_analysis import comparative_sentiment_analysis
from approach_library.utils.text_to_speech import text_to_speech
import os

# Function
def analyze_company_news(company):
    st.write(f"Analyzing company: {company}")
    
    with st.spinner("Fetching news articles..."):
        articles = extract_news(company)
        if not articles:
            st.error("No news articles found. Try a different company.")
            return None
        st.write(f"Found {len(articles)} articles")
    
    articles_data = []
    texts = [article["text"] for article in articles]
    
    with st.spinner("Performing sentiment analysis..."):
        sentiment_results = analyze_sentiment(texts)
        st.write(f"Sentiment analysis completed for {len(sentiment_results['Predicted Sentiment'])} articles")
    
    for article, sentiment in zip(articles, sentiment_results["Predicted Sentiment"]):
        summary = summarize_text(article["text"])
        preprocessed_text = preprocess_text([article["text"]])
        lda_model, dictionary = train_lda(preprocessed_text)
        topic_words = extract_topic_words(lda_model)
        
        articles_data.append({
            "Title": article["title"],
            "Summary": summary,
            "Sentiment": sentiment,
            "Topics": topic_words
        })
    
    with st.spinner("Performing comparative analysis..."):
        analysis_result = comparative_sentiment_analysis(company, articles_data)
        st.write("Comparative analysis completed")
        st.write("Analysis result:", analysis_result)
    
    final_summary = f"{company}’s latest news coverage is mostly {analysis_result['Final Sentiment Analysis']}."
    
    with st.spinner("Generating Hindi TTS summary..."):
        try:
            audio_file = text_to_speech(final_summary)
            if os.path.exists(audio_file):
                st.write(f"TTS summary generated: {audio_file}")
            else:
                st.error("Failed to generate TTS summary")
                audio_file = None
        except Exception as e:
            st.error(f"TTS generation failed: {str(e)}")
            audio_file = None
    
    return {
        "Company": company,
        "Articles": articles_data,
        "Comparative Sentiment Score": analysis_result,
        "Audio": audio_file
    }

st.title("Company News Analysis")
company = st.text_input("Enter the company name for analysis:")
if st.button("Analyze") and company:
    st.write(f"Starting analysis for: {company}")
    result = analyze_company_news(company)
    if result:
        st.subheader(f"Analysis for {result['Company']}")
        
        for article in result["Articles"]:
            st.write(f"**Title:** {article['Title']}")
            st.write(f"**Summary:** {article['Summary']}")
            st.write(f"**Sentiment:** {article['Sentiment']}")
            st.write(f"**Topics:** {', '.join(article['Topics'])}")
            st.markdown("---")
        
        st.subheader("Comparative Sentiment Score")
        st.json(result["Comparative Sentiment Score"])
        
        st.subheader("Hindi TTS Summary")
        if result["Audio"]:
            st.audio(result["Audio"], format="audio/mp3")
        else:
            st.warning("TTS summary not available")

