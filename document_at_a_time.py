from collections import namedtuple
from typing import Dict, List

Document = namedtuple('Document', 'id content length')
Term = namedtuple('Term', 'id word weight')
PostingListItem = namedtuple('PostingListItem', 'id doc_id word_id weight')

documents = [Document(0, 'ya,ru', 10), Document(1, 'google.com', 100), Document(3, 'kantiana.ru', 200)]
vocabulary = [Term(0, 'Россия', 1), Term(1, 'Англия', 1), Term(2, 'Америка', 1)]
posting_list = [PostingListItem(0, 0, 0, 3), PostingListItem(1, 0, 1, 4), PostingListItem(2, 1, 2, 2)]

query = 'Америка Англия'


def main():

    results = {}

    plists: Dict[int, PostingListItem] = {}
    for qt in query.split():
        for term in vocabulary:
            if qt == term.word:
                for pl in posting_list:
                    if pl.word_id == term.id:
                        plists[pl.doc_id] = pl

    cur_doc_id = None
    score = 0
    for doc_id, pl in sorted(plists.items()):
        if pl.doc_id != cur_doc_id:
            if cur_doc_id is not None:
                results[cur_doc_id] = score
            score = 0
            cur_doc_id = pl.doc_id
        if cur_doc_id is None:
            break

        word = None
        for w in vocabulary:
            if w.id == pl.word_id:
                word = w
                break

        if word is None:
            continue

        score += pl.weight * word.weight

    if cur_doc_id is not None:
        results[cur_doc_id] = score

    for doc_id, score in results.items():
        print(f'{doc_id}: {score}')


if __name__ == '__main__':
    main()
