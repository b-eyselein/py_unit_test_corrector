import copy
import os
from typing import List, Any


def is_number(s: Any) -> bool:
    """checks if a string can be converted to float"""
    try:
        float(s)
        return True
    except ValueError:
        return False


class Table:
    def __init__(self, name: str):
        self.name: str = name
        self.fields: List[str] = []
        self.data: List[List[str]] = []

    def load_from_csv(self, csv_file, delimiter=';'):
        # reset previous attributes
        self.data = []
        self.fields = []

        if not os.path.isfile(csv_file):
            raise Exception("File not found")

        with open(csv_file, 'r', encoding="utf-8-sig") as f:
            for idx, line in enumerate(f):
                # remove trailing new line, split by delimiter and set to lowercase
                line = line.rstrip("\n").lower()
                line = line.split(delimiter)
                # first line in file is treated as list of fields
                if idx == 0:
                    self.fields = line
                else:
                    self.data.append(line)

        # convert all number strings to floats
        for i, row in enumerate(self.data):
            for j, entry in enumerate(row):
                if is_number(entry):
                    self.data[i][j] = float(entry)

    def copy(self, original_table: 'Table'):
        self.fields = copy.deepcopy(original_table.fields)
        self.data = copy.deepcopy(original_table.data)

    def length(self) -> int:
        return len(self.fields)

    def insert(self, row) -> bool:
        if len(row) != self.length():
            raise Exception("Length of the row does not match table length!")
        else:
            # convert to floats:
            for i in range(len(row)):
                if is_number(row[i]):
                    row[i] = float(row[i])

            # check if data types are the same
            types_new = [type(a) for a in row]
            types_old = [type(a) for a in self.data[0]]
            if types_new != types_old:
                raise Exception("Data types of new row do not match old ones")

            # append the data
            self.data.append(row)
            return True
