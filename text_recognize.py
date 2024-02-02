import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
import heapq

nltk.download('punkt')
nltk.download('stopwords')

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

# Example usage
text = input("Enter your text: ")

num_sentences = 5
summary = text_summarizer(text, num_sentences)


print("\nSummary:")
print(summary)
