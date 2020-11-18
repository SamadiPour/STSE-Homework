import csv


class DatasetReader:
    test_csv = 'isarcasm_test.csv'
    train_csv = 'isarcasm_train.csv'

    def __init__(self):
        self.path = '../dataset/'

    def read_dataset(self, file):
        f = open(self.path + file, newline='')
        csv_reader = csv.reader(f)

        # Skip title row
        next(csv_reader)

        rows = []
        for row in csv_reader:
            rows.append(row)

        return rows
