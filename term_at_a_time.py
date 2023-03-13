from collections import namedtuple

Document = namedtuple('Document', 'id content length')
Term = namedtuple('Term', 'id word weight')
PostingListItem = namedtuple('PostingListItem', 'id doc_id word_id weight')

documents = [Document(0, 'ya,ru', 10), Document(1, 'google.com', 100), Document(3, 'kantiana.ru', 200)]
vocabulary = [Term(0, 'Россия', 1), Term(1, 'Англия', 1), Term(2, 'Америка', 1)]
posting_list = [PostingListItem(0, 0, 0, 3), PostingListItem(1, 0, 1, 4), PostingListItem(2, 1, 2, 2)]

query = 'Америка Англия'


def main():

    scored = {}
    for qt in query.split():
        word = None
        for w in vocabulary:
            if w.word == qt:
                word = w
                break
        for dt in posting_list:

            cur_doc = None
            for doc in documents:
                if doc.id == dt.doc_id:
                    cur_doc = doc
                    break

            if cur_doc is None:
                continue

            if dt.word_id == word.id:
                if dt not in scored:
                    scored[dt] = 0
                scored[dt] += word.weight * dt.weight / cur_doc.length


    for key, value in scored.items():
        print(f'{key}: {value}')


if __name__ == '__main__':
    main()

