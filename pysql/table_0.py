import os
import copy


def is_number(s):
    """checks if a string can be converted to float"""
    if type(s) == int:
        return float(s)
    elif type(s) == float:
        return s
    elif '_' in s:
        return False
    else:
        try:
            float(s)
            return True
        except ValueError:
            return False


class Table:
    def __init__(self, name):
        self.name = name
        self.fields = []
        self.data = []

    def load_from_csv(self, csv_file, delimiter=';'):
        # reset previous attributes
        self.data = []
        self.fields = []

        if os.path.isfile(csv_file):
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
        else:
            print("File not found")
            return

        # convert all number strings to floats
        for i, row in enumerate(self.data):
            for j, entry in enumerate(row):
                if is_number(entry):
                    self.data[i][j] = float(entry)

    def copy(self, original_table):
        self.fields = copy.deepcopy(original_table.fields)
        self.data = copy.deepcopy(original_table.data)

    def length(self):
        return len(self.fields)

    def insert(self, row):
        if len(row) != self.length():
            print("Length of the row does not match table length!")
            return False
        else:
            # convert to floats:
            for i in range(len(row)):
                if is_number(row[i]):
                    row[i] = float(row[i])
            # check if data types are the same
            types_new = [type(a) for a in row]
            types_old = [type(a) for a in self.data[0]]
            if types_new != types_old:
                print("Data types of new row do not match old ones")
                return False
            # append the data
            self.data.append(row)
            return True
