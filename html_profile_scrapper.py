
import sys
import requests
from lxml import html
from consts import Consts


class HtmlProfileScrapper:

    @staticmethod
    def add_info(logger, author_name, user_id, record_manager, job_manager):
        logger.log('parsing {author_name} profile..'.format(author_name=author_name))

        # download page
        page_url = Consts.BASE_ADDRESS + user_id
        with requests.get(page_url) as page:
            if page.status_code != 200:
                logger.error('got error code: {err_no}'.format(err_no=page.status_code))
                sys.exit(1)
            page_content = page.content

        # parse html
        tree = html.fromstring(page_content)

        # extract research field
        research_field = str(HtmlProfileScrapper.get_research_field(logger, tree))

        # handle citation history
        citation_history = HtmlProfileScrapper.get_citation_history(logger, tree)

        if citation_history is not None:    # and \
                # min(int(year_key) for year_key in citation_history.keys()) >= Consts.EARLIEST_CITATION_YEAR:
            # ignore authors that hers first citations is to early
            record_manager.add(author_name, research_field, citation_history)

        # handle co-authors
        co_author_list = HtmlProfileScrapper.get_co_author_list(logger, tree)
        if co_author_list is not None:
            for co_author_name in co_author_list.keys():
                job_manager.add(
                    '{co_author_name}{job_info_separator}{user_id}'.format(
                        co_author_name=co_author_name, job_info_separator=Consts.JOB_INFO_SEPARATOR,
                        user_id=co_author_list[co_author_name]
                    )
                )

    @staticmethod
    def get_research_field(logger, html_tree_root):
        container_class = r'gsc_prf_inta gs_ibl'

        # find research fields container tag
        fields = html_tree_root.xpath('//a[@class="{class_name}"]/text()'.format(class_name=container_class))
        if not fields:
            logger.error('can\'t find fields..')
            return False

        # check for CS related research fields
        lower_case_field_list = [x.lower() for x in Consts.VALID_FIELDS]
        for field_name in fields:
            if field_name.lower() in lower_case_field_list:
                return True
        return False

    @staticmethod
    def get_citation_history(logger, html_tree_root):
        year_tag_class_name = r'gsc_g_t'
        counter_tag_class_name = r'gsc_g_al'

        # find years
        years = html_tree_root.xpath('//span[@class="{class_name}"]/text()'.format(class_name=year_tag_class_name))
        if not years:
            logger.error('can\'t find years..')
            return None

        # find counter tags
        counters = html_tree_root.xpath('//span[@class="{class_name}"]/text()'.format(class_name=counter_tag_class_name))
        if not counters:
            logger.error('can\'t find counters..')
            return None
        elif len(years) != len(counters):
            logger.error('different number of years and counters')
            return None

        # build list of all counters
        int_counters = [int(x) for x in counters]

        # join years with counters
        year_counter = dict()
        for i in range(len(years)):
            year_counter[years[i]] = int_counters[i]

        return year_counter

    @staticmethod
    def get_co_author_list(logger, html_tree_root):
        container_tag_name = r'gsc_rsb_a_desc'
        co_authors = dict()

        # find containers
        container_tags = html_tree_root.xpath('//span[@class="{class_name}"]'.format(class_name=container_tag_name))
        if not container_tags:
            logger.log('no co-authors found')
            return co_authors

        # extract containers info
        for outer_tag in container_tags:
            child_nodes = outer_tag.getchildren()
            if not child_nodes:
                logger.error('missing tag child node')
                return co_authors

            for node in child_nodes:
                if node.tag == 'a':
                    # extract author name
                    author_name = node.text
                    # extract author profile page url
                    profile_url = node.get('href')
                    # add user id to co-author list
                    co_authors[author_name] = profile_url.split(r'citations?user=')[1]
                    break

        # return list
        return co_authors
