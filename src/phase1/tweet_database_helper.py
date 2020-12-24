import os
import sqlite3

from src.config import root_dir


class TweetDatabaseHelper:
    __table_name = 'tweets'

    def __init__(self, name) -> None:
        super().__init__()

        path = os.path.join(root_dir, 'dataset', f"{name}.db")
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

        self.__create()
        self.connection.commit()

    def add_item(self, tweet, sarcasm_label, sarcasm_type) -> bool:
        try:
            data_tuple = (
                tweet.id_str, tweet.user.id,
                tweet.user.screen_name, tweet.created_at,
                tweet.lang, tweet.full_text,
                sarcasm_label, sarcasm_type,
            )

            self.__insert(data_tuple)
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all(self):
        return self.cursor.execute(
            f"SELECT * FROM {TweetDatabaseHelper.__table_name};"
        ).fetchall()

    def get_distinct_users(self):
        return self.cursor.execute(
            f"SELECT distinct user_id FROM {TweetDatabaseHelper.__table_name};"
        ).fetchall()

    def __create(self):
        query = f"""
        create table IF NOT EXISTS {TweetDatabaseHelper.__table_name}
        (
            tweet_id          TEXT not null primary key unique,
            user_id           TEXT,
            username          TEXT,
            tweet_timestamp   TIMESTAMP,
            lang              TEXT,
            text              TEXT,
            sarcasm_label     TEXT,
            sarcasm_type      TEXT
        );
        """
        self.cursor.execute(query)

    def __insert(self, data):
        self.cursor.execute(
            f'INSERT INTO {TweetDatabaseHelper.__table_name} '
            f'VALUES (?, ?, ?, ?, ?, ?, ?, ?);',
            data
        )
