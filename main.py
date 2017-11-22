
from multiprocessing.dummy import Pool as ThreadPool
import time
from csv_manager import CsvManager
from job_manager import JobManager
from html_profile_scrapper import HtmlProfileScrapper
from logger import Logger


THREAD_POOL_SIZE = 10
MAX_TRIES = 3
TRY_WAIT_INTERVAL = 5


def scrapper_worker(arguments):
    # parse arguments
    logger, csv_manager, job_manager = arguments[0], arguments[1], arguments[2]

    logger.log('worker thread started')
    tries = 0
    while tries < MAX_TRIES:
        while job_manager.has_jobs():
            tries = 0
            job = job_manager.get_next().split('$$$')
            author_name = job[0]
            user_id = job[1]
            HtmlProfileScrapper.add_info(logger, author_name, user_id, csv_manager, job_manager)
        logger.log('no more jobs, waiting and checking again..')
        time.sleep(TRY_WAIT_INTERVAL)
        tries += 1
    logger.log('worker thread exit')


def main():
    logger = Logger()

    # create managers
    csv_manager = CsvManager()
    job_manager = JobManager(logger)

    # add first job
    author_name = r'Matthew E. Taylor'
    job_manager.add(
        r'{author_name}$$$edQgLXcAAAAJ'.format(author_name=author_name)
    )

    # test html parser
    logger.log('## begin threads run')
    thread_pool = ThreadPool(THREAD_POOL_SIZE)
    logger.log('wait for all threads to finish')
    thread_pool.map(scrapper_worker, [(logger, csv_manager, job_manager)] * THREAD_POOL_SIZE)
    thread_pool.close()
    thread_pool.join()
    logger.log('## threads done')

if __name__ == '__main__':
    main()
