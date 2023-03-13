from typing import Tuple, List, Iterator
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from collections import namedtuple

Page = namedtuple('Page', 'Id Url')

pages: List[Page] = []

max_doc_count = 10
alpha = 0.15

start_pages = ['https://kantiana.ru/']

mapped_pages: List[Tuple[int, float]] = []


def main() -> None:

    for url in start_pages:
        links = retrieve_hyperlinks(url)
        # for link in links:
        #     print(link)

    # print('----------------------------------------------')
    # print('Pages')
    # print('----------------------------------------------')
    # for page in pages:
    #     print(f'{page.Id}, {page.Url}')

    for page in pages:
        links = retrieve_hyperlinks(page.Url)
        values = 1.0, links

        for k, v in map_fn(page.Url, values):
            mapped_pages.append((k, v))

    for doc_id, parts in shuffler():
        rank, _ = reduce_fn(doc_id, parts)
        url = find_url_by_id(doc_id)
        print(f'{-rank} {url}')


def map_fn(link: str, v: Tuple[float, List[str]]) -> Iterator[Tuple[int, float]]:
    rank, outlinks = v

    doc_id = find_id(link)
    yield doc_id, 0.0

    if len(outlinks) > 0:
        for link in outlinks:
            d_id = find_id(link)
            yield d_id, rank / len(outlinks)
    else:
        for i in range(max_doc_count):
            yield i, rank / max_doc_count


def reduce_fn(doc_id: int, parts: List[float]) -> Tuple[float, int]:
    return - ( (1 - alpha) * sum(parts) + alpha / max_doc_count ), doc_id


def shuffler() -> Iterator[Tuple[int, List[int]]]:
    new_pages = sorted(mapped_pages)

    buffer = []
    prev_doc_id: int or None = None
    for doc_id, value in new_pages:
        if prev_doc_id == doc_id:
            buffer.append(value)
        else:
            if prev_doc_id is not None:
                yield prev_doc_id, buffer
            buffer = [value]
        prev_doc_id = doc_id

    if buffer:
        yield prev_doc_id, buffer


def find_id(link: str) -> int:

    for page in pages:
        if page.Url == link:
            return page.Id

    return -1


def find_url_by_id(id: int) -> str or None:

    for page in pages:
        if page.Id == id:
            return page.Url

    return None


def add_page(link: str):

    for page in pages:
        if page.Url == link:
            return

    new_page = Page(len(pages), link)
    pages.append(new_page)


def retrieve_hyperlinks(url: str) -> List[str]:

    http = httplib2.Http()
    status, response = http.request(url)

    lst: List[str] = []

    for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            href = link['href']
            if href.startswith("http") or href.startswith("https"):
                lst.append(href)
                add_page(href)

    return lst


if __name__ == '__main__':
    main()

