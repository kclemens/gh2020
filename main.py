


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
    def books(self, library_index):
        """
        returns the list of books_indexes in a library 
        """

    def signup_time(self, library_index):
        """
        returns the time to sign up that library for scanning
        """
        
    def concurrency_factor(self, library_index):
        """
        returns the number of books a library can scan in parallel 
        """

    def score(self, library_index):
        """
        returns the importance score of a library
        """

    def library_in_order(self):
        """
        returns the list of libraries ordered by their score
        """

class Scanner(object):
    pass

if __name__ == '__main__':
    with open('data/a_example.txt') as data:
        print data.next().split()
        for line in data:
            print line.strip()
