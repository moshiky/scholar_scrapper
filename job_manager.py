
import threading


class JobManager:

    def __init__(self, logger):
        self.__logger = logger
        self.__queue = list()
        self.__history = list()
        self.__data_lock = threading.Lock()

    def has_jobs(self):
        self.__logger.log('waiting jobs: {jobs_size}, passed: {history_size}'
                          .format(jobs_size=len(self.__queue), history_size=len(self.__history)))
        return len(self.__queue) > 0

    def add(self, item):
        with self.__data_lock:
            if self.__queue.count(item) == 0 and self.__history.count(item) == 0:
                self.__queue.append(item)

    def get_next(self):
        with self.__data_lock:
            if len(self.__queue) > 0:
                next_item = self.__queue[0]
                self.__queue = self.__queue[1:]
                self.__history.append(next_item)
                return next_item

            else:
                return None
