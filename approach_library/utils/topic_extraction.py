# Importing Libraries
from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import nltk

# Downloading necessary NLTK resources
nltk.download('all')
nltk.download('stopwords')
nltk.download('punkt_tab')

def preprocess_text(text_data):
    """
    Preprocesses text data by tokenizing, removing stopwords, punctuation, and non-alphabetic tokens.

    :param text_data: List of raw text documents
    :return: List of preprocessed tokenized texts
    """
    stop_words = set(stopwords.words("english"))
    processed_texts = [
        [
            word for word in word_tokenize(document.lower())
            if word not in stop_words and word not in string.punctuation and word.isalpha()
        ]
        for document in text_data
    ]
    return processed_texts

def train_lda(texts, num_topics=3):
    """
    Trains an LDA model on the given preprocessed text data.

    :param texts: List of tokenized texts
    :param num_topics: Number of topics for the LDA model
    :return: Trained LDA model and corresponding dictionary
    """
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    ldamodel = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
    
    return ldamodel, dictionary

def extract_topic_words(ldamodel, num_topics=3, num_words=3):
    """
    Extracts meaningful words from each topic identified by the LDA model.

    :param ldamodel: Trained LDA model
    :param num_topics: Number of topics to extract
    :param num_words: Number of words per topic to consider
    :return: List of top words representing each topic
    """
    topics = ldamodel.print_topics(num_topics=num_topics, num_words=num_words)
    topic_names = []

    for topic in topics:
        words = topic[1].split(" + ")
        for word_data in words:
            word = word_data.split("*")[1].strip('"')  # Extract word
            if word.isalpha() and len(word) > 2:  
                topic_names.append(word)
                break  # Only take the top valid word

    return list(set(topic_names)) 

