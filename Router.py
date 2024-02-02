from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from nltk.sentiment import SentimentIntensityAnalyzer
from application import app
import heapq


# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('vader_lexicon')


def text_summarizer(text, num_sentences):
    # Tokenize the text into sentencesˀ
    sentences = sent_tokenize(text)

    # Tokenize the text into words
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word.casefold() not in stop_words]

    # Perform stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]

    # Calculate the frequency of each word
    word_frequencies = FreqDist(words)

    # Calculate the weighted frequency of each sentence
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if len(sentence.split()) < 30:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]

    # Select the top N sentences with the highest scores
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)

    return summary

# Example usage ......................................................................
# text = input("Enter your text: ")

# num_sentences = 5
# summary = text_summarizer(text, num_sentences)


# print("\nSummary:")
# print(summary)




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

# Get user input.......................................................................
# user_input = input("Enter a word or phrase: ")

# Classify sentiment of the user input
# result = classify_sentiment(text)

# # Print the sentiment result
# print("Sentiment: " + result)





# routes................................................................. 
@app.route("/")
def index():
    return render_template("/Welcome.html")

@app.route("/main")
def main():
  return render_template("/Main.html")



@app.route("/summerize", methods=['POST'])
def process_summerization():
    data = request.get_json()  # Get the JSON data from the request
    text = data.get('text')    # Extract the 'text' property from the data

    num_sentences = 5
    summary = text_summarizer(text, num_sentences)

    # Process the received text or perform any desired actions
    # response_text = f{text}"

    # Create a response object
    response = {'message': summary}

    return jsonify(response)


@app.route("/sentiment", methods=['POST'])
def process_sentiment():
        data = request.get_json()  # Get the JSON data from the request
        text = data.get('text')    # Extract the 'text' property from the data

        # print(text)

        result = classify_sentiment(text)

        response = {'sentiment': result}

        return jsonify(response)