
import threading
import csv


class CsvManager:

    def __init__(self):
        self.__min_year = 1950
        self.__max_year = 2017
        self.__year_index = [str(x) for x in range(self.__min_year, self.__max_year+1, 1)]
        self.__create_file()
        self.__add_lock = threading.Lock()
        # todo: parse csv and load stored authors list

    def __create_file(self):
        record_row = ['author_name'] + self.__year_index
        with open('records.csv', 'wt') as results_csv_file:
            writer = csv.writer(results_csv_file)
            writer.writerow(record_row)

    def __format_history(self, history_to_pad):
        padded_history = dict()
        for year_id in self.__year_index:
            padded_history[year_id] = '0'
            if year_id in history_to_pad.keys():
                padded_history[year_id] = str(history_to_pad[year_id])

        return [x[1] for x in sorted(padded_history.items())]

    def add(self, author_name, citation_history):
        record_row = [author_name] + self.__format_history(citation_history)
        with self.__add_lock:
            with open('records.csv', 'at') as results_csv_file:
                writer = csv.writer(results_csv_file)
                try:
                    writer.writerow(record_row)
                except Exception as ex:
                    record_row[0] = '<invalid name>'
                    writer.writerow(record_row)
