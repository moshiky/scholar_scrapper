
import requests
from lxml import html

from csv_manager import CsvManager
from job_manager import JobManager
from html_profile_scrapper import HtmlProfileScrapper
from logger import Logger


def main():
    logger = Logger()

    # create managers
    csv_manager = CsvManager()
    job_manager = JobManager()

    # add first job
    author_name = r'Matthew E. Taylor'
    job_manager.add(
        r'{author_name}$$$https://scholar.google.com/citations?user=edQgLXcAAAAJ'.format(author_name=author_name)
    )

    # test html parser
    while job_manager.has_jobs():
        job = job_manager.get_next().split('$$$')
        author_name = job[0]
        page_url = job[1]
        HtmlProfileScrapper.add_info(logger, author_name, page_url, csv_manager, job_manager)

if __name__ == '__main__':
    main()
