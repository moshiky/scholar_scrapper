
import requests
from lxml import html
import os


class HtmlProfileScrapper:

    @staticmethod
    def add_info(logger, author_name, profile_page_url, record_manager, job_manager):
        logger.log('parsing {author_name} profile..'.format(author_name=author_name))

        # download page
        with requests.get(profile_page_url) as page:
            page_content = page.content

        # parse html
        tree = html.fromstring(page.content)

        # handle citation history
        citation_history = HtmlProfileScrapper.get_citation_history(logger, tree)
        if citation_history is not None:
            record_manager.add(author_name, citation_history)

        # handle co-authors
        co_author_list = HtmlProfileScrapper.get_co_author_list(logger, tree)
        if co_author_list is not None:
            for co_author_name in co_author_list.keys():
                job_manager.add(
                    '{co_author_name}$$${page_url}'.format(
                        co_author_name=co_author_name, page_url=co_author_list[co_author_name]
                    )
                )

    @staticmethod
    def get_citation_history(logger, html_tree_root):
        year_tag_class_name = r'gsc_g_t'
        counter_tag_class_name = r'gsc_g_a'

        # find years
        years = html_tree_root.xpath('//span[@class="{class_name}"]/text()'.format(class_name=year_tag_class_name))
        if not years:
            logger.error('can\'t find years..')
            return None

        # find citation counter tags
        counter_tags = html_tree_root.xpath('//a[@class="{class_name}"]'.format(class_name=counter_tag_class_name))
        if not counter_tags:
            logger.error('can\'t find counters..')
            return None
        elif len(years) != len(counter_tags):
            logger.error('different number of years and counters')
            return None

        # build list of all counters
        counters = list()
        for outer_tag in counter_tags:
            child_nodes = outer_tag.getchildren()
            if len(child_nodes) != 1:
                logger.error('missing counter tag child node / too many nodes')
                return None
            counters.append(int(child_nodes[0].text))

        # join years with counters
        year_counter = dict()
        for i in range(len(years)):
            year_counter[years[i]] = counters[i]

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
                    # add info to co-author list
                    co_authors[author_name] = os.path.join(r'https://scholar.google.com/', profile_url[1:])
                    break

        # return list
        return co_authors
