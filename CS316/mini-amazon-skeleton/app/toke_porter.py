
from nltk.stem.porter import PorterStemmer

porter = PorterStemmer()
def tokenizer_porter(text,stop = None):
    if type(stop) == type(None):
        return [porter.stem(word) for word in text.split()] 
    else :
        return [porter.stem(word) for word in text.split() if word not in stop] 
