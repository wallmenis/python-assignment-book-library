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
        
        self.books_df = self.books_df.set_index("ID")
        self.reviews_df = self.reviews_df.set_index("ID")

    def get_book_at_index(self, index):
        return Book(
            ID = index,
            title = self.books_df.loc[index, "title"],
            author = self.books_df.loc[index, "author"],
            publisher = self.books_df.loc[index, "publisher"],
            categories = self.books_df.loc[index, "categories"],
            cost = self.books_df.loc[index, "cost"],
            shipping_cost = self.books_df.loc[index, "shipping_cost"],
            availiability = self.books_df.loc[index, "availiability"]
            copies = self.books_df.loc[index, "copies"],
            bookstores = self.books_df.loc[index, "bookstores"]
            )

    def get_book_reviews_by_book(self, book):           # I am trying to abstract as much as possible because seeing
                                                        # the raw code with pandas will be hard to understand without
                                                        # excessive comments (or a painful read).
        return self.reviews_df.loc[reviews_df["book_id"] == book.ID]

    def get_book_reviews_by_user(self, user):
        return self.reviews_df.loc[reviews_df["user_id"] == user.ID]
    
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
