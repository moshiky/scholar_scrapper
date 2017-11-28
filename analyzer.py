
import sys
import csv
from consts import Consts


class Analyzer:

    def __init__(self, logger):
        self.__logger = logger

    def parse_records_file(self, file_path):
        # read file
        with open(file_path, 'rt') as file_handle:
            reader = csv.reader(file_handle)
            file_lines = list(reader)

        # parse into dict with user id keys
        # dict[<user_id>] = [<year_0_counter>, <year_1_counter>, ...]
        user_info = dict()
        for line in file_lines[1:]:
            if line[1] == 'True':   # is form our research field
                user_info[line[0]] = [int(x) for x in line[2:]]

        return user_info

    def calculate_total_publications_over_time(self, publication_data_file_path):
        # parse publications file
        publication_data = self.parse_records_file(publication_data_file_path)

        # for each user_id
        output_dict = dict()
        for user_id in publication_data.keys():
            last_year_pubs = 0
            output_dict[user_id] = list()
            for year_id in range(len(Consts.YEAR_INDEX)):
                # calculate total pubs until that year
                last_year_pubs += publication_data[user_id][year_id]
                # store rate in output dict
                output_dict[user_id].append(last_year_pubs)

        # store to output file
        csv_rows = [[user_id] + output_dict[user_id] for user_id in output_dict.keys()]
        with open(r'results/total_publications_over_time__{timestamp}.csv'.format(
                timestamp=publication_data_file_path.split('__')[1].replace('.csv', '')
        ), 'wt', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_rows)

    def calculate_citations_per_publications_over_time(self, citation_data_file_path, publication_data_file_path):
        # parse citations file
        citation_data = self.parse_records_file(citation_data_file_path)

        # parse publications file
        publication_data = self.parse_records_file(publication_data_file_path)

        # for each user_id
        output_dict = dict()
        for user_id in citation_data.keys():
            last_year_cits = 0
            last_year_pubs = 0
            output_dict[user_id] = list()
            for year_id in range(len(Consts.YEAR_INDEX)):
                # calculate total cits and pubs until that year
                last_year_cits += citation_data[user_id][year_id]
                last_year_pubs += publication_data[user_id][year_id]
                # store rate in output dict
                output_dict[user_id].append((float(last_year_cits)/last_year_pubs) if last_year_pubs > 0 else 0)

        # store to output file
        csv_rows = [[user_id] + output_dict[user_id] for user_id in output_dict.keys()]
        with open(r'results/citations_per_publications_over_time__{timestamp}.csv'.format(
                timestamp=citation_data_file_path.split('__')[1].replace('.csv', '')
                    ), 'wt', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_rows)


if __name__ == '__main__':
    analyzer = Analyzer(None)
    print('start analyze..')
    analyzer.calculate_total_publications_over_time(sys.argv[2])
    analyzer.calculate_citations_per_publications_over_time(sys.argv[1], sys.argv[2])
    print('done')
