import asyncio
import argparse
import aiohttp
from loguru import logger
from models.companies_contact_pages_model import CompaniesContactPageModel
from selectolax.parser import HTMLParser
import re

parser = argparse.ArgumentParser(description='Simple phone numbers scrapper')
parser.add_argument('--offset', type=int, default=0, help='Optional offset for database requests')
parser.add_argument('--limit', type=int, default=10, help='Optional limit for database requests')
parser.add_argument('--company', type=int, default=None, help='Optional company ID')
arguments = parser.parse_args()

# Regular expressions for phone numbers extraction
regexps_for_phone_numers = [
    re.compile(r"((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}", flags=re.MULTILINE|re.UNICODE)
]
regexp_euristic_filter = re.compile(r"\d+")


def prepare_urls():
    """
    Generate list of URLs
    :return:
    """
    query = CompaniesContactPageModel\
        .select().offset(arguments.offset)\
        .limit(arguments.limit)

    if isinstance(arguments.company, int):
        query = query.where(CompaniesContactPageModel.company_id == arguments.company)

    for record in query:
        yield record.url


def get_text_selectolax(html):
    """
    BeautifulSoup returns very dirty page content
    full of JS code and styles. This solution is a kind
    of fast workaround fot that problem - it returns almost clean
    page content
    :param html:
    :return:
    """
    tree = HTMLParser(html)

    if tree.body is None:
        return None

    for tag in tree.css('script'):
        tag.decompose()
    for tag in tree.css('style'):
        tag.decompose()

    text = tree.body.text(separator='\n')
    return text


async def handle_request(session, url):
    """
    Requesting and processing URL from server
    :param session:
    :param url:
    :return:
    """
    async with session.get(url) as resp:
        if resp.status == 200:
            logger.success(f'Got HTML body of {url}')
            clean_text = get_text_selectolax(await resp.text())
            return [url, clean_text]

        else:
            logger.error(f'{url} -> got bad response status: {resp.status}')
            return False


async def fetch(loop):
    """
    Handling list of URLs
    :param urls:
    :param loop:
    :return:
    """
    async with aiohttp.ClientSession(loop=loop) as session:
        for r in asyncio.as_completed([handle_request(session, url) for url in prepare_urls()]):
            result = await r
            if result is not False:
                for expression in regexps_for_phone_numers:
                    for match in expression.finditer(result[1]):
                        seems_like_phone = match.group()
                        if seems_like_phone and len(list(filter(lambda x: x.isdigit(), seems_like_phone))) in (7, 9, 10, 11):
                            logger.success(f'{result[0]} -> Got smth looking like a phone number: {seems_like_phone}')



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    the_results = loop.run_until_complete(
        fetch(loop)
    )
