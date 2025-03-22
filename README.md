---
title: News Summarisation And Sentiment Analysis
emoji: 🔥
colorFrom: yellow
colorTo: blue
sdk: streamlit
sdk_version: 1.43.2
app_file: app.py
pinned: false
short_description: ' Fetch the articles of the given company name '
---

# News_Summarisation_Sentiment_Analysis
This is a web-based application that extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi.


## Features
- Company-specific news extraction
- Advanced text summarization using Pegasus model
- Sentiment analysis with Hugging Face Model
- Topic extraction using LDA
- Comparative sentiment analysis
- Text-to-speech conversion in Hindi
- User-friendly Streamlit interface

## Project Structure


## Installation
1. Create a virtual environment:
```bash
python -m venv myenv
# Windows
myenv\Scripts\activate
```
2. Install dependencies:
   ``` bash
   pip install -r requirements.txt
   ```

3. Run the application
```
streamlit run app.py
```

4. Usage
   ```
##Enter a company name and click "Analyze" to get:
-->News articles
-->Summaries
-->Sentiment analysis
-->Topic distribution
-->Comparative analysis
-->Audio output in Hindi
##Technical Details
-->Frontend: Streamlit
-->NLP Models:
-->Pegasus for summarization
-->FinBERT for sentiment analysis
-->LDA for topic modeling
-->Audio Processing: GTTS for text-to-speech
-->Backend: FastAPI
##Requirements
-->Python 3.8+
-->CUDA (optional for GPU acceleration)
-->Internet connection for model downloads

##License
-->MIT License

##Acknowledgments
-->Hugging Face for NLP models
-->Streamlit for web interface
-->NLTK for text processing

  ```
