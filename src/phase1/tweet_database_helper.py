import sqlite3

class TweetDatabaseHelper:
    __table_name = 'tweets'

    def __init__(self, name) -> None:
        super().__init__()

        self.connection = sqlite3.connect(f'{name}.db')
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
