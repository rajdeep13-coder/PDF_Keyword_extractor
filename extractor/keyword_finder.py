import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize

class KeywordProcessor:
    def __init__(self):
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('punkt', quiet=True)  # For sentence tokenization
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
        vectorizer = TfidfVectorizer(max_features=top_n)
        X = vectorizer.fit_transform([' '.join(tokens)])
        return list(zip(vectorizer.get_feature_names_out(), X.toarray()[0]))

    def summarize_text(self, text, ratio=0.2):
        try:
            # Replacement for gensim.summarization.summarize
            sentences = sent_tokenize(text)
            if len(sentences) < 3:
                return text
            
            # Create a TF-IDF vectorizer
            vectorizer = TfidfVectorizer(stop_words='english')
            vectors = vectorizer.fit_transform([' '.join(self.preprocess_text(sent)) for sent in sentences])
            
            # Get sentence scores
            scores = {}
            for i, sent in enumerate(sentences):
                scores[i] = sum(vectors[i].toarray()[0])
            
            # Select top sentences
            num_sentences = max(1, int(len(sentences) * ratio))
            top_indices = sorted(scores, key=scores.get, reverse=True)[:num_sentences]
            
            # Return summary in original order
            summary_sentences = [sentences[i] for i in sorted(top_indices)]
            return ' '.join(summary_sentences)
            
        except Exception as e:
            return f"Summarization error: {str(e)}"