import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
import os
import re
from gensim.summarization import summarize

class KeywordProcessor:
    def __init__(self):
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        self.stopwords = self._load_stopwords()
        self.lemmatizer = WordNetLemmatizer()

    def _load_stopwords(self):
        custom_path = os.path.join('data', 'stopwords.txt')
        if os.path.exists(custom_path):
            with open(custom_path, 'r') as f:
                return set(f.read().splitlines())
        return set(stopwords.words('english'))

    def preprocess_text(self, text):
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        tokens = text.split()
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens 
                  if word not in self.stopwords and len(word) > 2]
        return tokens

    def get_keywords(self, text, method='frequency', top_n=25):
        clean_tokens = self.preprocess_text(text)
        if method == 'frequency':
            return Counter(clean_tokens).most_common(top_n)
        elif method == 'tfidf':
            return self._tfidf_analysis(clean_tokens, top_n)
        else:
            raise ValueError("Invalid method. Use 'frequency' or 'tfidf'.")

    def _tfidf_analysis(self, tokens, top_n):
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(max_features=top_n)
        X = vectorizer.fit_transform([' '.join(tokens)])
        return list(zip(vectorizer.get_feature_names_out(), X.toarray()[0]))

    def summarize_text(self, text, ratio=0.2):
        try:
            return summarize(text, ratio=ratio)
        except ValueError:
            return "Text too short or repetitive to summarize."
        except Exception as e:
            return f"Summarization error: {str(e)}"
