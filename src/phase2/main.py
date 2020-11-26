from src.config import *
from src.phase1.tweet_database_helper import TweetDatabaseHelper
from nltk.tokenize import RegexpTokenizer

if __name__ == '__main__':
    database = TweetDatabaseHelper(train_csv)
    for item in database.get_all()[:3]:
        text = item[5]
        print(text)

        # todo: remove user mention
        # todo: remove links
        # todo: remove html tags
        # todo: remove numbers
        # todo: make words lowercase
        # todo: remove extra @ " ٪ " + / ) ( = *
        # todo: fix typos
        # todo: remove stop words
        # todo: Normalization

        tk = RegexpTokenizer('\s+', gaps=True)
        tokens = tk.tokenize(text)
        print(tokens)
