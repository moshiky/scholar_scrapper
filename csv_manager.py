
import threading
import csv
import os
import time
from consts import Consts


class CsvManager:

    def __init__(self):
        self.__year_index = Consts.YEAR_INDEX

        # set file names
        timestamp_string = time.strftime('%d_%m_%Y__%H_%M_%S')
        self.__citations_file_name = \
            os.path.join(r'results', r'citations__{timestamp}.csv'.format(timestamp=timestamp_string))
        self.__publications_file_name = \
            os.path.join(r'results', r'publications__{timestamp}.csv'.format(timestamp=timestamp_string))

        # initiate file
        self.__create_files()
        self.__add_lock = threading.Lock()
        # todo: parse csv and load stored authors list

    def __create_files(self):
        record_row = ['author_name', 'research_field'] + self.__year_index

        # create citations file
        with open(self.__citations_file_name, 'wt', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(record_row)

        # create publications file
        with open(self.__publications_file_name, 'wt', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(record_row)

    def __format_history(self, history_to_pad):
        padded_history = dict()
        for year_id in self.__year_index:
            padded_history[year_id] = '0'
            if year_id in history_to_pad.keys():
                padded_history[year_id] = str(history_to_pad[year_id])

        return [x[1] for x in sorted(padded_history.items())]

    def add(self, author_name, research_field_type, citation_history, publication_history):

        with self.__add_lock:

            # add citation history record
            record_row = [author_name, research_field_type] + self.__format_history(citation_history)
            with open(self.__citations_file_name, 'at', newline='') as csv_file:
                writer = csv.writer(csv_file)
                try:
                    writer.writerow(record_row)
                except Exception as ex:
                    record_row[0] = '<invalid name>'
                    writer.writerow(record_row)

            # add publication history record
            record_row = [author_name, research_field_type] + self.__format_history(publication_history)
            with open(self.__publications_file_name, 'at', newline='') as csv_file:
                writer = csv.writer(csv_file)
                try:
                    writer.writerow(record_row)
                except Exception as ex:
                    record_row[0] = '<invalid name>'
                    writer.writerow(record_row)
