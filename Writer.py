import csv


class Writer(object):
    def __init__(self, file_name: str, header: list):
        self.f = open(file_name, 'w')
        self.writer = csv.writer(self.f)
        self.writer.writerow(header)
        self.file_name = file_name

    def close(self):
        self.f.close()

    def open(self):
        self.f = open(self.file_name, 'w')

    def write_row(self, values: list):
        self.writer.writerow(values)
        self.f.flush()
