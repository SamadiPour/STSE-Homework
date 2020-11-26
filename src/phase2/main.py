from src.logic.config import *
from src.phase1.tweet_database_helper import TweetDatabaseHelper

if __name__ == '__main__':
    database = TweetDatabaseHelper(train_csv)
    for item in database.get_all():
        print(item)
