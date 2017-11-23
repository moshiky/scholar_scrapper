
from multiprocessing.dummy import Pool as ThreadPool
import time
from csv_manager import CsvManager
from job_manager import JobManager
from html_profile_scrapper import HtmlProfileScrapper
from logger import Logger
from consts import Consts


def scrapper_worker(arguments):
    # parse arguments
    logger, csv_manager, job_manager = arguments[0], arguments[1], arguments[2]

    logger.log('worker thread started')
    tries = 0
    while tries < Consts.MAX_TRIES:
        while job_manager.has_jobs():
            tries = 0
            job = job_manager.get_next().split(Consts.JOB_INFO_SEPARATOR)
            author_name = job[0]
            user_id = job[1]
            HtmlProfileScrapper.add_info(logger, author_name, user_id, csv_manager, job_manager)
        logger.log('no more jobs, waiting and checking again..')
        time.sleep(Consts.TRY_WAIT_INTERVAL)
        tries += 1
    logger.log('worker thread exit')


def main():
    logger = Logger()

    # create managers
    csv_manager = CsvManager()
    job_manager = JobManager(logger)

    # add first job
    job_manager.add(
        r'{author_name}{job_info_separator}{user_id}'.format(
            author_name=Consts.FIRST_USER['name'], job_info_separator=Consts.JOB_INFO_SEPARATOR,
            user_id=Consts.FIRST_USER['user_id']
        )
    )

    # test html parser
    logger.log('## begin threads run')
    thread_pool = ThreadPool(Consts.THREAD_POOL_SIZE)
    logger.log('wait for all threads to finish')
    thread_pool.map(scrapper_worker, [(logger, csv_manager, job_manager)] * Consts.THREAD_POOL_SIZE)
    thread_pool.close()
    thread_pool.join()
    logger.log('## threads done')

if __name__ == '__main__':
    main()
