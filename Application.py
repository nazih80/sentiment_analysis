def clean_tweet(tweet):
    from re import sub,compile, UNICODE
    urlRE = r'[(http(s)?):\/\/(www\.)?a-z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-z0-9@:%_\+.~#?&//=]*)'
    hashtagRE = r'#[a-z0-9_]+'
    mentionRE = r'@[a-z0-9_]+'
    emojiRE = compile(
        "["u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"u"\U0001F1E0-\U0001F1FF""]+", flags=UNICODE)
    HTMLentitiesRE = r'&[a-z0-9#]+;'
    punctuationRE = r'[^\w\s]'
    tweet = sub(urlRE, "", tweet)
    tweet = sub(hashtagRE, "", tweet)
    tweet = sub(mentionRE, "", tweet)
    tweet = sub(emojiRE, "", tweet)
    tweet = sub(HTMLentitiesRE, "", tweet)
    tweet = sub(r'\n', ' ', tweet)
    tweet = sub(r'\brt\b', ' ', tweet)
    tweet = sub(punctuationRE, ' ', tweet)
    # Remplaces multiple spaces with one
    tweet = sub(r' +', ' ', tweet)
    # Removes all spaces from the start and etweet.strip()
    return tweet

def preprocess_tweet(tweet):
    import spacy
    nlp = spacy.load("en_core_web_md")
    doc = nlp(tweet)
    return " ".join([token.lemma_ for token in doc if not token.is_stop])

def predict_sentiment(tweet):
    from joblib import load
    model = load('SVM_model.joblib')
    vectorizer = load('vectorizer.joblib')
    prediction = model.predict(vectorizer.transform([tweet]))
    return prediction[0]

# Main function to get user input and display the predicted sentiment
def main():
    tweet = input("Enter the tweet: ")
    tweet = clean_tweet(tweet)
    tweet = preprocess_tweet(tweet)
    sentiment = predict_sentiment(tweet)
    if (sentiment == -1):
        print("Predicted sentiment: Negative")
    elif (sentiment == 0):
        print("Predicted sentiment: Neutral")
    else:
        print("Predicted sentiment: Positive")

if __name__ == '__main__':
    main()
