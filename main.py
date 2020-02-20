


class BookRegistry(object):
    def book_ids(self):
        """
        returns the list of available book ids
        """
        
    def value(self, book_id):
        """
        returns the weight of a book
        """

    def distribution(self, book_id):
        """
        returns the number of libraries that book is part of
        """

    def score(self, book_id):
        """
        returns the score of each book using value() and distribution() methods
        """
        
    def order(selfs, list_of_book_ids):
        """
        returns the indices from the given list, ordered by score from high to low 
        """


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

    def remove_books(self, library_id, book_id_list):
        for book_id in book_id_list:
            self.books[library_id].remove(book_id)

    def library_ids_in_order(self):
        """
        returns the list of libraries ordered by their score
        """
        library_ids = self.signup_times.keys()
        library_ids = sorted(library_ids, key=lambda library_id: self.score(library_id))

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
        self.library_queue = self.library_registry.libray_ids_in_order()
        self.submitted_book_ids = set()

    def step(self):
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

            self.library_registry.remove_books(library_id, books)
            self.library_books[library_id] += books

            print 'library {} submits {} books: {}'.format(library_id,
                                                                     library_registry.concurrency_factor(library_id),
                                                                     ', '.join(books))



if __name__ == '__main__':

    book_registry = BookRegistry()
    library_registry = LibraryRegisry(book_registry)

    with open('data/a_example.txt') as data:
        print data.next().split()  # books, libraries, days
        print data.next().split()  # book weights
        for library_id, line in enumerate(data):
            _, signup_time, concurrency_factor = map(int, line.split())
            books = set(map(int, data.next().split()))
            library_registry.add_library(library_id, signup_time, concurrency_factor, books)
