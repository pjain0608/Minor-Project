import nltk
nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize the sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Function to classify sentiment
def classify_sentiment(text):
    # Calculate sentiment scores
    sentiment_scores = sid.polarity_scores(text)

    # Classify sentiment based on the compound score
    if sentiment_scores['compound'] >= 0.05:
        return "Positive"
    elif sentiment_scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Get user input
user_input = input("Enter a word or phrase: ")

# Classify sentiment of the user input
result = classify_sentiment(user_input)

# Print the sentiment result
print("Sentiment: " + result)
