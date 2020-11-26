import logging

from progressbar import ProgressBar

from src.logic.api import API
from src.config import *
from src.logic.dataset_reader import DatasetReader
from src.phase1.tweet_database_helper import TweetDatabaseHelper

if __name__ == '__main__':
    # Config
    logging.basicConfig(filename='app.log', filemode='w', format='%(levelname)s - %(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')

    # Initialize
    api = API()
    dataset = DatasetReader(train_csv)
    database = TweetDatabaseHelper(test_csv)

    items = dataset.read_dataset()
    with ProgressBar(max_value=len(items) - 1, redirect_stdout=True) as bar:
        for index, item in zip(range(len(items)), items):
            # get tweet
            tweet = api.get_tweet_by_id(item[0])

            if tweet is not None:
                database.add_item(tweet, item[1], item[2])

            # update progress bar
            bar.update(index)
