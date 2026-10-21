import re
from typing import List

# Standard English stopwords list to avoid external download dependencies
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", 
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", 
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", 
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", 
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", 
    "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", 
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", 
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", 
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", 
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", 
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", 
    "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", 
    "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", 
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", 
    "yourself", "yourselves"
}

try:
    from nltk.stem import PorterStemmer
    _stemmer = PorterStemmer()
    def stem_word(w: str) -> str:
        return _stemmer.stem(w)
except ImportError:
    # Lightweight fallback suffix stripper if nltk is not installed
    def stem_word(w: str) -> str:
        for suffix in ("ing", "ly", "ed", "ious", "ies", "es", "s"):
            if w.endswith(suffix) and len(w) > len(suffix) + 2:
                return w[:-len(suffix)]
        return w

def preprocess_financial_text(text: str, remove_stopwords: bool = True, apply_stemming: bool = True) -> List[str]:
    """
    Standardized financial text preprocessing:
    1. Cleaning: Lowercasing and noise removal.
    2. Financial Tokenization: Preserves monetary symbols ($), percentages (%), 
       decimals (10.5), acronyms, and ticker entities.
    3. Stop-word removal: Eliminates conversational terms.
    4. Stemming: Reduces inflectional forms using Porter Stemmer.
    """
    text = text.lower()
    # Extract financial tokens: numbers, percentages, currency, decimals, tickers
    tokens = re.findall(r"\b[a-z0-9$%.-]+\b", text)
    
    processed = []
    for token in tokens:
        # Strip trailing punctuation artifacts
        token = token.strip(".-")
        if not token:
            continue
            
        if remove_stopwords and token in STOP_WORDS:
            continue
            
        if apply_stemming and not re.search(r"\d", token):
            token = stem_word(token)
            
        processed.append(token)
        
    return processed

if __name__ == "__main__":
    sample = "Investors hedging against 10.5% inflation risk purchased $5,000 in treasury bonds."
    print("Sample Input:", sample)
    print("Processed Tokens:", preprocess_financial_text(sample))
