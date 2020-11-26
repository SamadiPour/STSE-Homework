import csv
import os

from src.config import root_dir


class DatasetReader:
    def __init__(self, name):
        path = os.path.join(root_dir, 'dataset', f"{name}.csv")
        self.file = open(path, newline='')

    def read_dataset(self):
        csv_reader = csv.reader(self.file)

        # Skip title row
        next(csv_reader)

        rows = []
        for row in csv_reader:
            rows.append(row)

        return rows
