import pandas as pd
import numpy as np
import book_io as bo
import ast

class LibraryDB():
    def __init__(self):
        books_df_types = {  'ID' : int,
                            'title' : str,
                            'author' : str,
                            'publisher' : str,
                            'categories' : np.ndarray,
                            'cost' : float,
                            'shipping_cost' : float,
                            'availability' : bool,
                            'copies' : int,
                            'bookstores' : dict}
        reviews_df_types = {'ID' : int,
                            'book_id' : int,
                            "user_id" : int,
                            "rating" : int,
                            "contents" : str}
        
        orders_df_types = {'ID' : int,
                            'book_id' : int,
                            "user_id" : int,
                            "bookstore" : str,
                            "cost" : int}
        # user_books_df_types = {  'ID' : int,
        #                     'title' : str,
        #                     'author' : str,
        #                     'publisher' : str,
        #                     'categories' : np.ndarray,
        #                     'cost' : float,
        #                     'shipping_cost' : float,
        #                     'availability' : bool,
        #                     'copies' : int,
        #                     'bookstores' : dict,
        #                     'user_id' : int}
        
        self.books_df = pd.DataFrame({'ID' : [],
                                     'title' : [],
                                     'author' : [],
                                     'publisher' : [],
                                     'categories' : [],
                                     'cost' : [],
                                     'shipping_cost' : [],
                                     'availability' : [],
                                     'copies' : [],
                                     'bookstores' : []}).astype('object')

        self.reviews_df = pd.DataFrame({'ID' : [],
                                     'book_id' : [],
                                     'user_id' : [],
                                     'rating' : [],
                                     'contents' : []}).astype('object')
        self.orders_df = pd.DataFrame({'ID' : [],
                                     'book_id' : [],
                                     'user_id' : [],
                                     'bookstore' : [],
                                     'cost' : []}).astype('object')
        # self.user_books_df = pd.DataFrame({'ID' : [],
        #                              'title' : [],
        #                              'author' : [],
        #                              'publisher' : [],
        #                              'categories' : [],
        #                              'cost' : [],
        #                              'shipping_cost' : [],
        #                              'availability' : [],
        #                              'copies' : [],
        #                              'bookstores' : [],
        #                              'user_id' : []}).astype('object')
        try:
            self.books_df = pd.read_csv("../data/books.csv").astype('object')
        except OSError:
            print("Failed to find/read books.csv file. Continuing with empty DataFrame")
        try:
            self.reviews_df = pd.read_csv("../data/reviews.csv").astype('object')
        except OSError:
            print("Failed to find/read reviews.csv file. Continuing with empty DataFrame")
        try:
            self.orders_df = pd.read_csv("../data/orders.csv").astype('object')
        except OSError:
            print("Failed to find/read orders.csv file. Continuing with empty DataFrame")
        # try:
        #     self.user_books_df = pd.read_csv("../data/user_books.csv").astype('object')
        # except OSError:
        #     print("Failed to find/read user_books.csv file. Continuing with empty DataFrame")
        
        self.books_df = self.books_df.set_index("ID")
        self.reviews_df = self.reviews_df.set_index("ID")
        self.orders_df = self.orders_df.set_index("ID")
        # self.user_books_df = self.user_books_df.set_index("ID")
        
        # def to_str_list(lis):
        #     result = []
        #     lis = ast.literal_eval(lis)
        #     for i in lis:
        #         result.append(str(i))
        #     return result
        # def to_dict_list(lis):
        #     result = []
        #     lis = ast.literal_eval(lis)
        #     result = lis
        #     for i in lis.keys():
        #         result[i] = int(result[i])
        #     return result
        def to_int_list(lis):
            if not pd.isna(lis):
                return ast.literal_eval(lis)
            return []
        self.books_df['categories'] = self.books_df['categories'].apply(to_int_list)
        self.books_df['bookstores'] = self.books_df['bookstores'].apply(to_int_list)
        def to_str(lis):
            if pd.isna(lis):
                return ""
            return str(lis)
        self.reviews_df['contents'] = self.reviews_df['contents'].apply(to_str)
        #self.user_books_df['categories'] = self.user_books_df['categories'].apply(to_int_list)
        #self.user_books_df['bookstores'] = self.user_books_df['bookstores'].apply(to_int_list)

        #print(self.books_df['categories'])
    
    # def get_custom_book_by_user_id(self,user_id):
    #     return self.user_books_df.loc[self.user_books_df['user_id'] == user_id]
    
    def check_if_book_real(self, title, author, publisher):
        found_real = True
        if self.books_df.loc[self.books_df['title'] == title].empty:
            found_real = False
        if self.books_df.loc[self.books_df['author'] == author].empty:
            found_real = False
        if self.books_df.loc[self.books_df['publisher'] == publisher].empty:
            found_real = False
        return found_real
        
    # def add_custom_book(self, title, author, publisher, categories, user_id):
    #     if not self.check_if_book_real(title, author, publisher, categories):
    #         if self.user_books_df.empty:
    #             tmp_id = -1
    #         else:
    #             tmp_id = self.user_books_df.index[self.user_books_df.shape[0]-1] - 1
    #         self.user_books_df.loc[tmp_id] = {'title' : title,
    #                                         'author' : author,
    #                                         'publisher' : publisher,
    #                                         'categories' : categories,
    #                                         'cost' : 0,
    #                                         'shipping_cost' : 0,
    #                                         'availability' : False,
    #                                         'copies' : 0,
    #                                         'bookstores' : dict(),
    #                                         'user_id' : user_id
    #                                         }
    #         return tmp_id

    def get_book_at_index(self, index):
        return Book(
            ID = index,
            title = self.books_df.loc[index, "title"],
            author = self.books_df.loc[index, "author"],
            publisher = self.books_df.loc[index, "publisher"],
            categories = self.books_df.loc[index, "categories"],
            cost = self.books_df.loc[index, "cost"],
            shipping_cost = self.books_df.loc[index, "shipping_cost"],
            availability = self.books_df.loc[index, "availability"],
            copies = self.books_df.loc[index, "copies"],
            bookstores = self.books_df.loc[index, "bookstores"]
            )
    
    def fix_copies(self, index):
        bookstores = self.books_df.loc[index]['bookstores'].keys()
        rez = 0
        for i in bookstores:
            rez = rez + self.books_df.loc[index]['bookstores'][i]
        self.books_df.at[index, 'copies'] = rez
        if rez <= 0:
            self.books_df.at[index, 'availability'] = False
    
    def get_books_by_categories(self,categories):
        categories_st = set(categories)
        categ = []
        for index, row in self.books_df:
            if categories_st.issubset(set(row["categories"])):
                categ.append(index)
        return books_df.loc[categ]
    
    def get_orders_by_user_id(self, uid):
        return self.orders_df.loc[self.orders_df['user_id'] == uid]
    
    def return_book_with_order_id(self, index):
        cost = self.orders_df.loc[index]['cost']
        bookstore = self.orders_df.loc[index]['bookstore']
        book_id = self.orders_df.loc[index]['book_id']
        user_id = self.orders_df.loc[index]['user_id']
        self.books_df.loc[book_id]['bookstores'][bookstore] = self.books_df.loc[book_id]['bookstores'][bookstore] + 1
        self.books_df.loc[book_id,'copies'] = self.books_df.loc[book_id]['copies'] + 1
        self.orders_df = self.orders_df.drop(index = index)
        tmp_rev_df = self.reviews_df
        tmp_rev_df = tmp_rev_df.loc[tmp_rev_df["user_id"] == user_id]
        tmp_rev_df = tmp_rev_df.loc[tmp_rev_df["book_id"] == book_id]
        for i in list(tmp_rev_df.index):
            self.remove_review_with_ID(i)
        return cost
    
    def return_book_with_order_id_return_user_id(self, index):
        cost = self.orders_df.loc[index]['cost']
        bookstore = self.orders_df.loc[index]['bookstore']
        book_id = self.orders_df.loc[index]['book_id']
        user_id = self.orders_df.loc[index]['user_id']
        self.books_df.loc[book_id]['bookstores'][bookstore] = self.books_df.loc[book_id]['bookstores'][bookstore] + 1
        self.books_df.loc[book_id,'copies'] = self.books_df.loc[book_id]['copies'] + 1
        self.orders_df = self.orders_df.drop(index = index)
        tmp_rev_df = self.reviews_df
        tmp_rev_df = tmp_rev_df.loc[tmp_rev_df["user_id"] == user_id]
        tmp_rev_df = tmp_rev_df.loc[tmp_rev_df["book_id"] == book_id]
        for i in list(tmp_rev_df.index):
            self.remove_review_with_ID(i)
        return cost, user_id
    
    def get_books_no_thought(self, orders):
        final_books = pd.DataFrame(self.books_df)
        # orders = self.get_orders_by_user_id(user_id)
        print(orders)
        for i in orders:
            final_books = final_books.drop(index = i)
        real_books = []
        # for i in favorites:
        #     if i > 0:
        #         real_books.append(i)
        # final_books = final_books.drop(index = real_books)
        return final_books
    
    def order_book_with_index_from_bookstore(self, index, bookstore, user_id):
        if self.books_df.loc[index]['bookstores'][bookstore] < 1 or not self.books_df.loc[index]['availability']:
            return 0.0
        
        self.books_df.loc[index]['bookstores'][bookstore] = self.books_df.loc[index]['bookstores'][bookstore] - 1
        self.books_df.loc[index,'copies'] = self.books_df.loc[index]['copies'] - 1
        if self.books_df.loc[index]['copies'] < 1:
            self.books_df.at[index, 'availability'] = False
        order_dict ={   'book_id' : index ,
                        'user_id' : user_id,
                        'bookstore' : bookstore,
                        'cost' : self.books_df.loc[index]['cost'] + self.books_df.loc[index]['shipping_cost']
                    }
        if self.orders_df.empty:
            tmp_id = 0
        else:
            tmp_id = self.orders_df.index[self.orders_df.shape[0]-1] + 1
        self.orders_df.loc[tmp_id] = order_dict
        return self.books_df.loc[index]['cost'] + self.books_df.loc[index]['shipping_cost']
    
    def get_all_bookstores(self):
        bookstores_st = set()
        for index, row in self.books_df.iterrows():
            bookstores_st = bookstores_st.union(set(row["bookstores"].keys()))
        return list(bookstores_st)
    
    def get_all_authors(self):
        authors_st = set()
        for index, row in self.books_df.iterrows():
            authors_st.add(row['author'])
        authors = []
        return list(authors_st)
    
    def get_all_publishers(self):
        publisher_st = set()
        for index, row in self.books_df.iterrows():
            publisher_st.add(row['publisher'])
        return list(publisher_st)
    
    def get_num_books_by_author(self):
        all_authors = self.get_all_authors()
        num_of_books = {}
        num_of_books_with_copies = {}
        for i in all_authors:
            bk = self.books_df.loc[self.books_df['author'] == i]
            num_of_books[i] = bk.shape[0]
            num_of_books_with_copies[i] = np.sum(bk['copies'])
        return num_of_books, num_of_books_with_copies
    
    def get_num_books_by_bookstores(self):
        all_bookstores = self.get_all_bookstores()
        num_of_books = dict(zip(all_bookstores, np.zeros(len(all_bookstores))))
        num_of_books_with_copies = dict(zip(all_bookstores, np.zeros(len(all_bookstores))))
        for i in all_bookstores:
            bk_by_bks = self.get_books_by_bookstores([i])
            num_of_books[i] = bk_by_bks.shape[0]
            for index, row in bk_by_bks.iterrows():
                bks_df = row['bookstores']
                num_of_books_with_copies[i] = num_of_books_with_copies[i] + bks_df[i]
        # num_of_books_with_copies = {bks: 0 for bks in all_bookstores}
        # bk_by_bks = self.get_books_by_bookstores(all_bookstores)
        # for i in all_bookstores:
        #     bk = bk_by_bks[i]
        #     num_of_books[i] = bk.shape[0]
        #     for j, row in bk.iterrows():
        #         num_of_books_with_copies[i] = row['bookstores'].get(i, 0)
        return num_of_books, num_of_books_with_copies
    
    def get_num_books_by_publisher(self):
        all_publishers = self.get_all_publishers()
        num_of_books = {}
        num_of_books_with_copies = {}
        for i in all_publishers:
            bk = self.books_df.loc[self.books_df['publisher'] == i]
            num_of_books[i] = bk.shape[0]
            num_of_books_with_copies[i] = np.sum(bk['copies'])
        return num_of_books, num_of_books_with_copies
    
    def get_distribution_by_avail_books(self):
        bk = self.books_df.loc[self.books_df['availability'] == True]
        bk = pd.DataFrame(bk)
        result = {}
        bk['total_cost'] = bk['cost'] + bk['shipping_cost']
        #bk = bk.sort_values(by = ['total_cost'], axis = 0, kind = "quicksort")
        #max_price = bk.iloc[-1]['total_cost']
        max_price = np.max(bk['total_cost'])
        print(max_price)
        # print(bk)
        # i = 0
        # while i < bk.shape[0]:
        #     result[bk.iloc[i]["title"]] = bk.iloc[i]['total_cost']
        #     i = i + 1
        # for index, row in bk.iterrows():
        #     result["(" + str(index) + ") " + row["title"]] = row['total_cost']
        
        rg_input=5
        n_ranges = 0
        ranges=[0]
        i = 0
        while i < rg_input - 1:
            n_ranges = np.round(max_price/rg_input + n_ranges, decimals = 2) 
            ranges.append(n_ranges)
            i = i + 1
        ranges.append(np.ceil(max_price))
        
        franges=[]
        i = 0
        while i < len(ranges) - 1:
            franges.append([ranges[i], ranges[i + 1]])
            i = i + 1
        
        for i in franges:
            result[str(i[0]) + ".." + str(i[1])] = 0
        
        for i in franges:
            for index, row in bk.iterrows():
                
                if i[0] < row["total_cost"] and i[1] >= row["total_cost"] :
                    print(str(row["total_cost"]) + " " + str(i))
                    result[str(i[0]) + ".." + str(i[1])] = result[str(i[0]) + ".." + str(i[1])] + 1
        
        return result
    
    def get_cost_books_by_author(self, author):
        bk = self.books_df.loc[self.books_df['author'] == author]
        cost_of_books=np.sum(bk['cost'])
        cost_of_books_by_copy=np.sum(bk['cost']*bk['copies'])
        return cost_of_books , cost_of_books_by_copy
    
    def get_cost_books_by_publisher(self, publisher):
        bk = self.books_df.loc[self.books_df['publisher'] == publisher]
        cost_of_books=np.sum(bk['cost'])
        cost_of_books_by_copy=np.sum(bk['cost']*bk['copies'])
        return cost_of_books , cost_of_books_by_copy
    
    def get_cost_books(self):
        bk = self.books_df
        cost_of_books=np.sum(bk['cost'])
        cost_of_books_by_copy=np.sum(bk['cost']*bk['copies'])
        return cost_of_books , cost_of_books_by_copy
            
    
    def get_book_as_dict(self, index):
        return dict(zip(self.books_df.columns,self.get_book_at_index(index).export_as_list()[1:]))
    
    def add_book(self, book):
        new_id = 0
        if self.books_df.empty:
            new_id = 0
        else:
            new_id = self.books_df.index[self.books_df.shape[0]-1] + 1
        # self.books_df = pd.concat([pd.DataFrame(book.export_as_list(), columns = self.books_df.columns), self.books_df])
        self.books_df.loc[new_id] = dict(zip(self.books_df.columns,book.export_as_list()[1:]))
        self.fix_copies(new_id)
        
    def add_review(self, review_dict):
        if self.reviews_df.empty:
            tmp_id = 0
        else:
            tmp_id = self.reviews_df.index[self.reviews_df.shape[0]-1] + 1
        self.reviews_df.loc[tmp_id] = review_dict
    
    def edit_book(self, book):
        if not self.books_df.empty:
            book.calculate_cost_avail()
            self.books_df.loc[book.ID] = dict(zip(self.books_df.columns,book.export_as_list()[1:]))
            return True
        return False

    def get_book_reviews_by_book(self, book):           # I am trying to abstract as much as possible because seeing
                                                        # the raw code with pandas will be hard to understand without
                                                        # excessive comments (or a painful read).
        return self.reviews_df.loc[reviews_df["book_id"] == book.ID]

    def get_book_reviews_by_user_ID(self, user_id):
        return self.reviews_df.loc[reviews_df["user_id"] == user_id]
    
    def get_book_reviews_by_user(self, user):
        return self.reviews_df.loc[reviews_df["user_id"] == user.ID]
    
    def get_book_review_ub(self, book, user):
        tmp_df = self.get_book_reviews_by_book(book)
        return self.get_book_reviews_by_user(user)
    
    def remove_book_with_ID(self, ID):
        # if ID < 0:
        #     self.user_books_df = self.user_books_df.drop(index = ID)
        #     return True
        
        # toremove = self.reviews_df.loc[self.reviews_df["book_id"] == ID].index
        # if not toremove.empty:
        #     for i in 
        #     self.reviews_df = self.reviews_df.drop(index = toremove)
        #     return True
        if not self.books_df.loc[ID].empty:
            self.books_df = self.books_df.drop(index = ID)
            return True
        return False
#         toremove = self.orders_df.loc[self.orders_df["book_id"] == ID].index
#         if not toremove.empty:
#             for i in list(toremove) : 
#                 self.return_book_with_order_id(i)
#             
#             return True
#         return False
        
    def get_books_by_name(self, string):
        return self.books_df.loc[self.books_df["title"].str.contains(string, case=False)]
    
    def get_books_by_name_and_bookstore(self, string, bookstores):
        df = self.get_books_by_bookstores(bookstores)
        return self.df.loc[self.df["title"].str.contains(string, case=False)]

    def remove_book(self, book):
        return self.remove_book_with_ID(book.ID)
        
    def remove_review(self, review):
        return self.remove_review_with_ID(review.ID)
    
    def remove_review_with_ID(self, ID):
        if not self.reviews_df.loc[ID].empty:
            self.reviews_df = self.reviews_df.drop(index = ID)
            return True
        return False
    
    def remove_review_with_user_ID(self, ID):
        toremove = self.reviews_df.loc[self.reviews_df["user_id"] == ID]
        if not toremove.empty:
            self.reviews_df = self.reviews_df.drop(index = toremove)
            return True
        return False
    
    def save_to_path(self,path):
        self.books_df.to_csv(path + "/books.csv")
        # self.user_books_df.to_csv(path + "/user_books.csv")
        self.reviews_df.to_csv(path + "/reviews.csv")
        self.orders_df.to_csv(path + "/orders.csv")
    
    def save_books_csv(self):
        self.books_df.to_csv("../data/books.csv")
    
    # def save_user_books_csv(self):
    #     self.user_books_df.to_csv("../data/user_books.csv")
    
    def save_reviews_csv(self):
        self.reviews_df.to_csv("../data/reviews.csv")
    
    def save_orders_csv(self):
        self.orders_df.to_csv("../data/orders.csv")
        
    def import_new_books(self, csv_path):
        books_to_import = pd.DataFrame(columns=self.books_df.columns)
        try:
            books_to_import = pd.read_csv(csv_path).astype('object')
            # return
        except OSError:
            print("Failed to read file")
            return False
        books_to_import = books_to_import.set_index("ID")
        books_to_import['categories'] = books_to_import['categories'].apply(lambda x : ast.literal_eval(x))
        books_to_import['bookstores'] = books_to_import['bookstores'].apply(lambda x : ast.literal_eval(x))
        #print(books_to_import)
        #print(self.books_df.tail(1).index)
        rows = list(self.books_df.tail(1).index)[0] + 1
        if books_to_import.columns.all() == self.books_df.columns.all():
            for index, row in books_to_import.iterrows():
                if not self.check_if_book_real(row["title"], row["author"], row["publisher"]):
                    self.books_df.loc[rows] = row
                    print("Adding book " + row["title"] + " at " + str(rows))
                    rows = rows + 1
                else:
                    print("Didn't add book " + row["title"])
                    #self.books_df = pd.concat([books_to_import, self.books_df])
                #self.books_df = self.books_df.reset_index().drop_duplicates(subset='ID').set_index('ID')
            return True
        return False
    
    def get_books_by_bookstores(self, bookstores):
        result = pd.DataFrame(columns= self.books_df.columns)
#         st_bookstores = set(bookstores)
#         indices = {bks: [] for bks in st_bookstores}
#         for bks in bookstores:
#             for i, row in self.books_df.iterrows():
#                 st_book_bks = set(row["bookstores"].keys())
#                 if bks in st_book_bks:
#                     indices[bks].append(i)
#                     
#         result = {}
#         for bks, bks_indices in indices.items():
#             result[bks] = self.books_df.loc[bks_indices]
        for index, row in self.books_df.iterrows():
            row_bks = row["bookstores"]
            row_bks = list(row_bks.keys())
            toinclude = False
            for i in bookstores:
                if i in row_bks:
                    toinclude = True
            if toinclude:
                result.loc[index] = row
        return result
    
    def get_books_by_bookstores_exclusive(self, bookstores):
        result = pd.DataFrame(columns= self.books_df.columns)
        for index, row in self.books_df.iterrows():
            row_bks = row["bookstores"]
            row_bks = list(row_bks.keys())
            toinclude = True
            for i in row_bks:
                if not i in bookstores:
                    toinclude = False
            if toinclude:
                result.loc[index] = row
        return result
    
    def export_books_to_csv(self, csv_path):
        self.books_df.to_csv(csv_path)


def get_books_by_name_with_df(df, string):
    return df.loc[df["title"].str.contains(string, case=False)]

    
class Book():  # The data types of each value of the object are strictly following the requirements of the assignment
    def __init__(self, ID=-1,
                 title="I",
                 author="do",
                 publisher="not",
                 categories=["exist"],
                 cost=-1.0,
                 shipping_cost=-1.0,
                 availability = False,
                 copies=-1,
                 bookstores={"here" : -1}):
        self.ID = ID
        self.title = title
        self.author = author
        self.publisher = publisher
        self.categories = categories
        self.cost = cost
        self.shipping_cost = shipping_cost
        self.availability = availability
        self.copies = copies
        self.bookstores = bookstores

    def export_as_list(self):
        return [self.ID,
                self.title,
                self.author,
                self.publisher,
                self.categories,
                self.cost,
                self.shipping_cost,
                self.availability,
                self.copies,
                self.bookstores]
        
    def get_total_cost(self):
        return self.cost + self.shipping_cost
    
    def import_from_dict(dictionary):
        self.ID = dictionary["ID"]
        self.title = dictionary["title"]
        self.author = dictionary["author"]
        self.publisher = dictionary["publisher"]
        self.categories = dictionary["categories"]
        self.cost = dictionary["cost"]
        self.shipping_cost = dictionary["shipping_cost"]
        self.availability = dictionary["availability"]
        self.copies = dictionary["copies"]
        self.bookstores = dictionary["bookstores"]
    
    def print_me(self):
        print(f"Title: {self.title} (ID {self.ID})")
        print()
        print()
        print(f"Author: {self.author}\t\tPublisher: {self.publisher}")
        print(f"Cost: {self.cost}\t\tShipping Cost: {self.shipping_cost}")
        print(f"Total cost: {self.get_total_cost()}")
        if self.availability:
            print("Is availiable.")
        else:
            print("Not availiable.")
        print("Copies per bookstore:")
        bo.print_dict(self.bookstores)
        
    def calculate_cost_avail(self):
        if self.copies < 1:
            self.availability = False