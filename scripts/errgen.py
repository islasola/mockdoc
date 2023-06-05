import json, csv

class ErrorGenerator:
    def __init__(self):
        self.errcode = './erroref/errcode.csv'
        self.grouping = './erroref/grouping.csv'
        self.errors = self.__prepare_errorcode()
        self.groups = self.__prepare_grouping()

    def __prepare_errorcode(self):
        errors = {}
        with open(self.errcode, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                errors[row[0]] = row[1]

        return errors

    def __prepare_grouping(self):
        groups = {}
        with open(self.grouping, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] not in groups:
                    groups[row[0]] = []
                groups[row[0]].append(row[1])

        for group in groups:
            groups[group] = list(set(groups[group])).sort()

        return groups
    
    def get_errorcode_desc(self, error_code):
        return self.errors[error_code]


    