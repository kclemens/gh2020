


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
        score = sum of book score * relative delay * concurrency factor
        """
        score = sum(map(lambda book_id: self.book_registry.score(book_id), self.books[library_id]))
        score *= self.signup_times[library_id] / max(self.signup_times.values())
        score *= self.concurrency_factors[library_id]

        return score

    def books(self, library_id):
        """
        returns the books in the library
        """
        return self.books[library_id]

    def library_ids_in_order(self):
        """
        returns the list of libraries ordered by their score
        """
        library_ids = self.signup_times.keys()
        library_ids = sorted(library_ids, key=lambda library_id: self.score(library_id))

        return library_ids


class Scanner(object):
    pass


if __name__ == '__main__':

    book_registry = BookRegistry()
    library_registry = LibraryRegisry(book_registry)

    with open('data/a_example.txt') as data:
        print data.next().split()  # books, libraries, days
        print data.next().split()  # book weights
        for library_id, line in enumerate(data):
            _, signup_time, concurrency_factor = map(int, line.split())
            books = map(int, data.next().split())
            library_registry.add_library(library_id, signup_time, concurrency_factor, books)
