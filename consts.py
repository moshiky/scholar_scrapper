
import time


class Consts:

    FIRST_USER = {
        'name': 'Matthew E. Taylor',
        'user_id': 'edQgLXcAAAAJ'
    }

    VALID_FIELDS = [
        'artificial intelligence',
        'intelligent agents',
        'multi-agent systems',
        'reinforcement learning',
        # 'robotics',
        # 'computer science',
        'machine learning',
        'neural networks',
        'Human-Level Machine Intelligence',
        'Image processing',
        'Computer vision',
        'Pattern recognition',
        'data mining',
        # 'Computer Graphics',
        'Data Analysis'
    ]

    BASE_ADDRESS = r'http://scholar.google.co.il/citations?user='

    JOB_INFO_SEPARATOR = '$$$'

    EARLIEST_CITATION_YEAR = 2007

    THREAD_POOL_SIZE = 2
    MAX_TRIES = 3
    TRY_WAIT_INTERVAL = 5

    BUFFERING_STEP_SIZE = 100

    FILE_CHECK_INTERVAL = 60

    FIRST_YEAR = 1970
    CURRENT_YEAR = time.localtime().tm_year
    YEAR_INDEX = [str(x) for x in range(FIRST_YEAR, CURRENT_YEAR+1, 1)]

    CONNECTION_ERROR_INTERVAL = 10
    CONNECTION_ERROR_TRIES = 5
