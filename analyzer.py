
import sys
import csv
from consts import Consts


class Analyzer:

    def __init__(self, logger):
        self.__logger = logger

    def align_careers(self, file_path):
        users_info = self.parse_records_file(file_path, only_our=True)
        no_zeros_dict = dict()
        for user_id in users_info.keys():
            current_index = 0
            while users_info[user_id][current_index] == 0:
                current_index += 1
            no_zeros_dict[user_id] = users_info[user_id][current_index:]

        # store to output file
        csv_rows = [[user_id] + no_zeros_dict[user_id] for user_id in no_zeros_dict.keys()]
        with open(r'results/no_zeros__{file_name}'.format(
                file_name=file_path[
                            len(file_path) - file_path[::-1].find(r'/') if file_path.find(r'/') > -1
                            else len(file_path) - file_path[::-1].find('\\') if file_path.find('\\') > -1
                            else 0
                            :
                          ]
        ), 'wt', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_rows)

    def parse_records_file(self, file_path, only_our=True):
        # read file
        with open(file_path, 'rt') as file_handle:
            reader = csv.reader(file_handle)
            file_lines = list(reader)

        # parse into dict with user id keys
        # dict[<user_id>] = [<year_0_counter>, <year_1_counter>, ...]
        user_info = dict()
        for line in file_lines[1:]:
            if not only_our or line[1] == 'True':   # is form our research field
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
    # analyzer.calculate_total_publications_over_time(sys.argv[2])
    # analyzer.calculate_citations_per_publications_over_time(sys.argv[1], sys.argv[2])
    analyzer.align_careers(sys.argv[1])
    print('done')
