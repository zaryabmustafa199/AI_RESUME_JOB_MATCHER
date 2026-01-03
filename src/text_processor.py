import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string

# Ensure NLTK data is downloaded (run these once or put in a setup script)
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """
    Performs basic text preprocessing: lowercasing, punctuation removal,
    number removal, tokenization, stop word removal, and lemmatization.

    Args:
        text (str): The raw input text.

    Returns:
        str: The cleaned and preprocessed text.
    """
    if not isinstance(text, str):
        return "" # Handle non-string input gracefully

    text = text.lower() # Lowercasing

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Tokenization
    tokens = nltk.word_tokenize(text)

    # Stop word removal
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return " ".join(tokens)