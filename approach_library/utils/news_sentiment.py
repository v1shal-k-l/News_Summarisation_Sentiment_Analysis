# Importing Libraries
import torch
import scipy.special
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load Hugging Face model and tokenizer
ckpt = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(ckpt)
model = AutoModelForSequenceClassification.from_pretrained(ckpt).to("cuda" if torch.cuda.is_available() else "cpu")

def analyze_sentiment(text_list):
    """Performs sentiment analysis on a list of texts using FinBERT."""
    preds = []
    preds_proba = []
    
    tokenizer_kwargs = {"padding": True, "truncation": True, "max_length": 512}
    
    for text in text_list:
        with torch.no_grad():
            # Tokenize the input
            input_sequence = tokenizer(text, return_tensors="pt", **tokenizer_kwargs).to(model.device)
            logits = model(**input_sequence).logits.cpu().numpy().squeeze()
            
            # Convert logits to probabilities
            scores = {
                k: v for k, v in zip(
                    model.config.id2label.values(),
                    scipy.special.softmax(logits)
                )
            }
            
            # Get the most probable sentiment
            sentiment = max(scores, key=scores.get)
            probability = max(scores.values())

            # Map the sentiment labels
            if sentiment == 'LABEL_2':
                sentiment = 'positive'
            elif sentiment == 'LABEL_0':
                sentiment = 'negative'
            else:
                sentiment = 'neutral'

            preds.append(sentiment)
            preds_proba.append(probability)

    # Return a DataFrame with results
    df_results = pd.DataFrame({
        "Text": text_list,
        "Predicted Sentiment": preds,
        "Probability": preds_proba
    })

    return df_results