import pandas as pd

class LibraryDB():
    def __init__(self):
        self.books_df = pd.DataFrame({'ID' : [],
                                     'title' : [],
                                     'authors' : [],
                                     'publisher' : [],
                                     'categories' : [],
                                     'cost' : [],
                                     'shipping_cost' : [],
                                     'availiability' : [],
                                     'copies' : [],
                                     'bookstores' : []}).astype('object')

        self.reviews_df = pd.DataFrame({'ID' : [],
                                     'book_id' : [],
                                     'user_id' : [],
                                     'contents' : []}).astype('object')
        try:
            self.books_df = pd.read_csv("../data/books.csv").astype('object')
        except OSError:
            print("Failed to find/read books.csv file. Continuing with empty DataFrame")
        try:
            self.reviews_df = pd.read_json("../data/reviews.json").astype('object')
        except OSError:
            print("Failed to find/read reviews.json file. Continuing with empty DataFrame")

    def get_book_at_index(self, index):
        return Book(
            ID = self.books_df.iat[index, 0],
            title = self.books_df.iat[index, 1],
            author = self.books_df.iat[index, 2],
            publisher = self.books_df.iat[index, 3],
            categories = self.books_df.iat[index, 4],
            cost = self.books_df.iat[index, 5],
            shipping_cost = self.books_df.iat[index, 6],
            availiability = self.books_df.iat[index, 7]
            copies = self.books_df.iat[index, 8],
            bookstores = self.books_df.iat[index, 9]
            )

    def get_book_reviews_by_book(self, book):           # I am trying to abstract as much as possible because seeing
                                                        # the raw code with pandas will be hard to understand without
                                                        # excessive comments (or a painful read).
        return self.books_df.loc[book.ID,'book_id']

    def get_book_reviews_by_user(self, user):
        return self.books_df.loc[user.ID,'user_id']
    
    def get_book_review_ub(self, book, user):
        tmp_df = get_book_reviews_by_book(book)
        return get_book_reviews_by_user(user)
    
class Book():  # The data types of each value of the object are strictly following the requirements of the assignment
    def __init__(self, ID=-1,
                 title="I",
                 author="do",
                 publisher="not",
                 categories=["exist"],
                 cost=-1.0,
                 shipping_cost=-1.0,
                 copies=-1,
                 bookstores={"here" : -1}):
        self.ID = ID
        self.title = title
        self.author = author
        self.publisher = publisher
        self.categories = categories
        self.cost = cost
        self.shipping_cost = shipping_cost
        self.bookstores = bookstores
