


class BookRegistry(object):
    def __init__(self):
        self.book_id_to_weight = dict()
        self.book_id_to_library = dict()

    def add_book(self, book_id, weight):
        self.book_id_to_weight[book_id] = weight

    def update_library(self, book_id, library_id):
        library = self.book_id_to_library.get(book_id, list())
        self.book_id_to_weight[book_id] = library.append(library_id)

    def book_ids(self):
        """
        returns the list of available book ids
        """
        return self.book_id_to_weight.keys()

    def value(self, book_id):
        """
        returns the weight of a book
        """
        return self.book_id_to_weight.get(book_id)

    def distribution(self, book_id):
        """
        returns the number of libraries that book is part of
        """
        return len(self.book_id_to_library.get(book_id))


    def score(self, book_id):
        """
        returns the score of each book using value() and distribution() methods
        """
        return self.value(book_id) / self.distribution(book_id)

    def order(self, list_of_book_ids):
        """
        returns the indices from the given list, ordered by score from high to low
        """
        return sorted(list_of_book_ids, key=lambda book_id: self.score(book_id), reverse=True)


class LibraryRegisry(object):
    def __init__(self, book_registry):
        self.book_registry = book_registry
        self.signup_times = dict()
        self.concurrency_factors = dict()
        self.books = dict()

    def add_library(self, library_id, signup_time, concurrency_factor, books):
        self.signup_times[library_id] = signup_time
        self.concurrency_factors[library_id] = concurrency_factor
        self.books[library_id] = books

    def score(self, library_id):
        """
        returns the importance score of a library
        score = sum of book score * relative delay * concurrency factor TODO: improvement potential
        """
        score = sum(map(lambda book_id: self.book_registry.score(book_id), self.books[library_id]))
        score *= self.signup_times[library_id] / max(self.signup_times.values())
        score *= self.concurrency_factors[library_id]

        return score

    def time_in_registration(self, library_id):
        """
        returns the time to register the given library
        """
        return self.signup_times[library_id]

    def concurrency_factor(self, library_id):
        """
        returns the number of books the given library can scan in parallel
        """
        return self.concurrency_factors[library_id]

    def books(self, library_id):
        """
        returns the books in the library
        """
        return self.books[library_id]

    def remove_books(self, book_id_list):
        for books in self.books.values():
            for book_id in book_id_list:
                books.remove(book_id)  # TODO: improvement potential -- reorder libraries to register next!

    def library_ids_in_order(self):
        """
        returns the list of libraries ordered by their score
        """
        library_ids = self.signup_times.keys()
        library_ids = sorted(library_ids, key=lambda library_id: self.score(library_id), reverse=True)

        for library_id in library_ids:
            yield library_id


class Scanner(object):
    def __init__(self, book_registry, library_registry, days):
        self.book_registry = book_registry
        self.library_registry = library_registry

        self.library_books = dict()
        self.library_order = list()
        self.days = days
        self.day = 0
        self.in_registration = None
        self.in_registration_time_left = 0
        self.library_queue = self.library_registry.library_ids_in_order()
        self.submitted_book_ids = set()

    def next(self):
        print 'day {}'.format(self.day)

        if self.day == self.days:
            raise StopIteration

        # start day
        self.day += 1

        # start registration of next library or update day count
        if not self.in_registration or not self.in_registration_time_left:
            if self.in_registration:
                self.library_order.append(self.in_registration)
                self.library_books[self.in_registration] = list()

            library_id = self.library_queue.next()
            self.in_registration = library_id
            self.in_registration_time_left = self.library_registry.time_in_registration()
        else:
            self.in_registration_time_left -= 1

        # append books to submit from each library in their order TODO: improvement potential
        for library_id in self.library_order:
            books = self.book_registry.order(self.library_registry.books(library_id))
            books = books[:self.library_registry.concurrency_factor(library_id)]

            self.library_registry.remove_books(books)
            self.library_books[library_id] += books

            print 'library {} submits {} books: {}'.format(library_id,
                                                           library_registry.concurrency_factor(library_id),
                                                           ', '.join(books))

        return self.day

if __name__ == '__main__':

    book_registry = BookRegistry()
    library_registry = LibraryRegisry(book_registry)

    with open('data/a_example.txt') as data:
        _, _, days = map(int, data.next().split())

        for book_id, book_weight in enumerate(data.next().split()):
            book_registry.add_book(book_id, int(book_weight))

        for library_id, line in enumerate(data):
            _, signup_time, concurrency_factor = map(int, line.split())
            books = set(map(int, data.next().split()))
            for book in books:
                book_registry.update_library(book, library_id)

            library_registry.add_library(library_id, signup_time, concurrency_factor, books)

    scanner = Scanner(book_registry, library_registry, days)
    while True:
        scanner.next()