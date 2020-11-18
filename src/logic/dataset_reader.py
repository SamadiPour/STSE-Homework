import csv


class DatasetReader:
    def __init__(self):
        self.path = '../dataset/'
        self.test_csv_name = 'isarcasm_test.csv'
        self.train_csv_name = 'isarcasm_train.csv'

    def read_test_dataset(self):
        f = open(self.path + self.test_csv_name, newline='')
        csv_reader = csv.reader(f)

        # Skip title row
        next(csv_reader)
        return csv_reader

    def read_train_dataset(self):
        f = open(self.path + self.train_csv_name, newline='')
        csv_reader = csv.reader(f)

        # Skip title row
        next(csv_reader)
        return csv_reader

