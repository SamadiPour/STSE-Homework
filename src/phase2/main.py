import re
import unicodedata

import contractions as contractions
import emoji
import nltk
from autocorrect import Speller
from nltk.tokenize.casual import reduce_lengthening

from src.config import *
from src.phase1.tweet_database_helper import TweetDatabaseHelper

if __name__ == '__main__':
    database = TweetDatabaseHelper(train_csv)

    # nltk.download('stopwords')
    # nltk.download('punkt')
    # nltk.download('wordnet')
    # nltk.download('wordnet_ic')
    # nltk.download('sentiwordnet')

    punctuations = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
    spell = Speller()

    for item in database.get_all():
        text = item[5]
        # print(text)

        # Make words lowercase
        text = text.lower()

        # Fix contractions  (you're -> you are)
        text = contractions.fix(text)

        # Remove usernames
        text = re.sub(r'(^|[^@\w])@(\w{1,15})\b', '', text).strip()

        # Remove links
        text = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b'
                      r'([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', '', text).strip()

        # Remove html tags
        text = re.sub(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', text).strip()

        # Remove Emojis
        text = re.sub("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U0001F1F2-\U0001F1F4"  # Macau flag
                      u"\U0001F1E6-\U0001F1FF"  # flags
                      u"\U0001F600-\U0001F64F"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U0001F1F2"
                      u"\U0001F1F4"
                      u"\U0001F620"
                      u"\u200d"
                      u"\u2640-\u2642"
                      "]+", '', text)
        text = ''.join([char for char in text if char not in emoji.UNICODE_EMOJI]).strip()

        # Replace unusual chars
        text = re.sub(r'’', '\'', text).strip()
        text = re.sub(r'[“”]', '\"', text).strip()

        # Remove extra @ " ٪ " + / ) ( = *
        text = ''.join([char for char in text if char not in punctuations])
        # print(text)

        # Tokenize
        words = nltk.tokenize.word_tokenize(text)

        # Remove non-ASCII characters from list of tokenized words
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            if new_word != '':
                new_words.append(new_word)
        words = new_words

        # Remove numbers
        words = [x for x in words if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]

        # Fix typos
        # words = [spell(reduce_lengthening(word)) for word in words]

        # Remove stop words
        stop_words = nltk.corpus.stopwords.words('english')
        words = [word for word in words if word not in stop_words]

        # Normalization
        porter = nltk.stem.PorterStemmer()
        words = [porter.stem(word) for word in words]

        print(words)
        # print("------------------------")
