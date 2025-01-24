import re

def clean_text(text):
    # Remove HTML Tags
    text = re.sub(r'<[^>]*>', '', text)
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove special characters
    text = re.sub(r'[^A-Za-z0-9]+', ' ', text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Trim leading and trailing spaces
    text = text.strip()
    # Remove extra white spaces
    text = ' '.join(text.split())
    return text