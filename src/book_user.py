import pandas as pd
import book_io as bo
import book_library_management as blm
import book_authentication as ba
import numpy as np
import ast
import random as rd

class UserDB():
    

    
    
    def __init__(self):
        user_df_types = {'ID' : int,
                        'username' : str,
                        'password' : str,
                        'address' : str,
                        'city' : str,
                        'orders' : object,
                        'favorites' : object,
                        'balance' : float}
        
        admin_df_types = {'ID' : int,
                        'username' : str,
                        'password' : str,
                        'bookstores' : object}
    
        self.user_df = pd.DataFrame({'ID' : [],
                                     'username' : [],
                                     'password' : [],
                                     'address' : [],
                                     'city' : [],
                                     'orders' : [],
                                     'favorites' : [],
                                     'balance' : []}).astype(user_df_types)

        self.admin_df = pd.DataFrame({'ID' : [],
                                      'username' : [],
                                      'password' : [],
                                      'bookstores' : []}).astype(admin_df_types)
        try:
            self.user_df = pd.read_csv("../data/users.csv").astype(user_df_types)
        except OSError:
            print("Failed to find/read books.csv file. Continuing with empty DataFrame")
        try:
            self.admin_df = pd.read_csv("../data/admins.csv").astype(admin_df_types)
        except OSError:
            print("Failed to find/read admins.csv file. Continuing with empty DataFrame")
            
        self.user_df = self.user_df.set_index("ID")
        self.admin_df = self.admin_df.set_index("ID")
        
        # print(type(self.user_df.loc[1,'favorites']))
        
        def to_int_list(lis):
            if not pd.isna(lis):
                return ast.literal_eval(lis)
            return []
        self.user_df['favorites'] = self.user_df['favorites'].apply(to_int_list)
        self.user_df['orders'] = self.user_df['orders'].apply(to_int_list)
        self.admin_df['bookstores'] = self.admin_df['bookstores'].apply(to_int_list)
        # print(self.user_df['favorites'][1])
        
    def save_dataframes(self):
        self.user_df.to_csv("../data/users.csv")
        self.admin_df.to_csv("../data/admins.csv")
        
    def add_admin_to_dataframe(self, admin):
        if not self.get_admin_by_username(admin.username).empty :
            return False
        tmp_admin = admin
        if self.admin_df.empty:
            tmp_admin.ID = 1
        else:
            tmp_admin.ID = self.admin_df.index[self.admin_df.shape[0]-1] + 1
        self.admin_df.loc[tmp_admin.ID] = dict(zip(self.admin_df.columns,admin.export_as_list()[1:]))
        # self.admin_df = pd.concat([pd.DataFrame(admin.export_as_list(),  columns = self.admin_df.columns), self.admin_df])
        return True
    
    def get_all_cities(self):
        city_st = set()
        for index, row in self.user_df.iterrows():
            city_st.add(row['city'])
        return list(city_st)
    
    def get_num_users_by_city(self):
        cities = self.get_all_cities()
        citi = {}
        for i in cities:
            citi[i] = self.user_df.loc[self.user_df["city"] == i].shape[0]
        return citi, cities

    def add_user_to_dataframe(self, user):
        if not self.get_user_by_username(user.username).empty:
            return False
        tmp_user = user
        if self.user_df.empty:
            tmp_user.ID = 1
        else:
            tmp_user.ID = self.user_df.index[self.user_df.shape[0]-1] + 1
        self.user_df.loc[tmp_user.ID] = dict(zip(self.user_df.columns,user.export_as_list()[1:]))
        return True
    
    def remove_admin_from_dataframe(self, admin):
        if not self.admin_df.loc[admin.ID].empty:
            self.admin_df = self.admin_df.drop(index = admin.ID)
            return True
        return False
    
    def remove_user_from_dataframe_ID(self, ID):
        if not self.user_df.loc[ID].empty:
            self.user_df = self.user_df.drop(index = ID)
            return True
        return False
    
    def remove_user_from_dataframe(self, user):
        if not self.user_df.loc[user.ID].empty:
            self.user_df = self.user_df.drop(index = user.ID)
            return True
        return False
    
    def edit_user_in_dataframe(self, user):
        if not self.user_df.loc[user.ID].empty:
            self.user_df.loc[user.ID] = dict(zip(self.user_df.columns,user.export_as_list()[1:]))
            return True
        return False
    
    def edit_admin_in_dataframe(self, admin):
        if not self.admin_df.loc[admin.ID].empty:
            self.admin_df.loc[admin.ID] = dict(zip(self.admin_df.columns,admin.export_as_list()[1:]))
            return True
        return False
        
    def get_user_by_username(self, username):
        return self.user_df.loc[self.user_df["username"] == username]
    
    def get_admin_by_username(self, username):
        return self.admin_df.loc[self.admin_df["username"] == username]


class User():
    def __init__(self,
                 ID=-1,
                 username="Do",
                 password="I",
                 address="Not",
                 city="Exist",
                 orders=[-1],
                 favorites=[-1],
                 balance = -1.0):
        self.ID = ID
        self.password = password
        self.username = username
        self.address = address
        self.city = city
        self.orders = orders
        self.favorites = favorites
        self.balance = balance
        self.auther = None
        
    def set_auther(self, auther ):
        self.auther = auther
    
    def check_book_avail(self):
        real_favorites = []
        fake_favorites = []
        for i in self.favorites:
            if i > 0:
                real_favorites.append(i)
            else:
                fake_favorites.append(i)
        books_to_show = self.auther.librarydb.books_df.loc[real_favorites]
        ids_to_select = bo.print_dataframe(books_to_show,
                           df_name = "books",
                           df_fields = ['title', 'author'],
                           df_title = "Please select books to view availiability of",
                           df_search_term="IDs",
                           use_search = True
                           )
        if ids_to_select == []:
            print("No book selected.")
        ids_to_select_int = []
        for i in ids_to_select:
            ids_to_select_int.append(int(i))
        
        ids_to_select = []
        for i in ids_to_select_int:
            if not i in list(books_to_show.index):
                print("Excluding " + i)
            else:
                ids_to_select.append(i)
        
        books_to_show = books_to_show.loc[ids_to_select]
        books_to_show = books_to_show.loc[books_to_show["availiability"] == True]
        
        print("Below books are availiable")
        print(books_to_show[["title","cost"]])
    
    def show_recommendations(self):
        book_categories = set()
        for index, row in self.auther.librarydb.books_df.iterrows():
            for i in row["categories"]:
                book_categories.add(i)
        counter = dict(zip(list(book_categories), np.zeros(len(list(book_categories)))))
        #user = users_df.loc[user_id]
        #print(user)
        book_ids_to_recommend = []
        for i in self.favorites:
            if i > -1 :
                book_ids_to_recommend.append(i)
        
        for i in self.orders:
            book_ids_to_recommend.append(i)
                
        for j in book_ids_to_recommend:
            for i in self.auther.librarydb.books_df.loc[j]["categories"]:
                counter[i] += 1
                
        max_category = list(counter.keys())[0]
        
        for i in list(counter.keys()):
            if counter[i] > counter[max_category]:
                max_category = i
        
        # books_to_recommend = self.auther.librarydb.get_books_by_categories(max_category)
                
        books_to_recommend = pd.DataFrame(self.auther.librarydb.books_df)
        
        for j in book_ids_to_recommend:
            books_to_recommend = books_to_recommend.drop(index = j)
        
        
        for index, row in pd.DataFrame(books_to_recommend).iterrows():
            if not max_category in row["categories"]:
                books_to_recommend = books_to_recommend.drop(index = index)
        
        books_to_recommend = books_to_recommend.reset_index()
                
        print(f"We recommend trying \"{books_to_recommend.loc[rd.randint(0, books_to_recommend.shape[0])]["title"]}\" out")
    
    def check_balance(self):
        print(f"Your balance is {self.balance}$")
        print("Would you like to add more funds?[Y/n]")
        inp = input()
        if inp == "Y":
            print("Please enter the amount to be added.")
            inp = input()
            self.balance = self.balance + float(inp)
            self.auther.userdb.edit_user_in_dataframe(self)

    def add_books_to_favorites(self):
        print("Please insert the IDs of the books you want to add to favorites (comma separated)")
        inp = bo.list_editor_int(self.favorites, "favorites", False)
        set_inp = set(inp)
        print("Would you like to add a custom book?[Y/N]")
        inp = input()
        if inp == "Y":
            dict_to_send = {'title' : "",
            'author' : "",
            'publisher' : "",
            'categories' : []}
            dict_to_send = bo.dict_editor(dict_to_send)
            self.auther.librarydb.add_custom_book(dict_to_send['title'], dict_to_send['author'], dict_to_send['publisher'], dict_to_send["publisher"], self.ID)
            fake_books_to_show = self.auther.librarydb.get_custom_book_by_user_id(self.ID)
            for index, row in fake_books_to_show.iterrows():
                self.favorites.append(index)
        print(self.favorites)
        new_favorites_set = set(self.favorites).union(set_inp)
        self.favorites = []
        for i in new_favorites_set:
            self.favorites.append(i)
        print(self.favorites)
        self.auther.userdb.edit_user_in_dataframe(self)
    
    def modify_account(self):
        dictionary = bo.dict_editor_custom({
        "ID" : self.ID,
        "username":self.username,
        "password":self.password,
        "address":self.address,
        "city":self.city,
        "orders":self.orders,
        "favorites":self.favorites}, ["username", "address","city"])
        self.username = dictionary["username"]
        self.address = dictionary["address"]
        self.city = dictionary["city"]
        print("Would you like to change your password?[Y/n]")
        inp = input()
        if inp == "Y":
            self.password = ba.password_register()
        self.auther.userdb.edit_user_in_dataframe(self)
    
    def order_book(self):
        # books = self.auther.librarydb.get_books_no_thought(self.ID, self.favorites)
        books = self.auther.librarydb.get_books_no_thought(self.orders)
        books_to_order = bo.print_dataframe( df = books,
                                            df_name = "books",
                                            df_fields = ["title", "author", "cost", "shipping_cost"],
                                            df_title = "Please search the books you would like to order",
                                            use_search = True,
                                            df_search_term = "title",
                                            interval = 10
                                            )
        if books_to_order == "":
            return
        final_books = pd.DataFrame(columns=books.columns)
        for i in books_to_order:
            final_books = pd.concat([blm.get_books_by_name_with_df(books, i), final_books])
        if final_books.shape[0] > 1:
            book_to_order = bo.print_dataframe(  df = final_books,
                                                df_name = "book",
                                                df_fields = ["title", "author", "cost", "shipping_cost"],
                                                df_title = "Please select the ID of the books you would like to order.",
                                                use_search = True,
                                                df_search_term = "ID",
                                                interval = 10,
                                                multiple = False
                                                )
            if book_to_order == "":
                return
        if not book_to_order == []:
            book_to_order = int(book_to_order)
            if not set(final_books.index.values).issuperset(set([book_to_order])):
                print("Invalid Index. Please try again.")
            else:
                book = self.auther.librarydb.get_book_at_index(book_to_order)
                if book.shipping_cost + book.cost > self.balance:
                    print("Insufficient funds.")
                else:
                    print("Please select bookstore:")
                    num = 1
                    for i in book.bookstores.keys():
                        print(f"{num} : {i}")
                        num = num + 1
                    inp = input()
                    inp = int(inp)
                    
                    bk = list(book.bookstores.keys())[inp-1]
                    cost = self.auther.librarydb.order_book_with_index_from_bookstore(book.ID, bk, self.ID)
                    if cost == 0.0:
                        print("Book is not availiable from this bookstore")
                        return
                    self.balance = self.balance - cost
                    self.orders.append(book.ID)
                    self.auther.userdb.edit_user_in_dataframe(self)
                    print("You have now ordered the below book.")
                    book.print_me()
                    
    def return_book(self):
        orders = self.auther.librarydb.get_orders_by_user_id(self.ID)
        print(orders)
        orders_to_return = bo.print_dataframe( df = orders,
                                            df_name = "books",
                                            df_fields = [ "book_id","cost"],
                                            df_title = "Please search the order you would like to return",
                                            use_search = True,
                                            df_search_term = "title",
                                            interval = 10
                                            )
        orders_to_return_int = []
        for i in orders_to_return:
            orders_to_return_int.append(int(i))
        for i in orders_to_return_int:
            self.balance = self.balance + self.auther.librarydb.return_book_with_order_id(i)
            k = 0
            while k < len(self.orders):
                if self.orders[k] == i:
                    self.orders.pop(k)
                else:
                    k += 1
            self.auther.userdb.edit_user_in_dataframe(self)
            
    def remove_books_from_favorites(self):
        real_favorites = []
        fake_favorites = []
        for i in self.favorites:
            if i > 0:
                real_favorites.append(i)
            else:
                fake_favorites.append(i)
        books_to_show = self.auther.librarydb.books_df.loc[real_favorites]
        # fake_books_to_show = self.auther.librarydb.get_custom_book_by_user_id(self.ID)
        fake_books_to_show = self.auther.librarydb.user_books_df.loc[fake_favorites]
        fake_books_to_show = fake_books_to_show.drop(labels = 'user_id', axis = 1 )
        books_to_show = pd.concat([books_to_show,fake_books_to_show])
        ids_to_remove = bo.print_dataframe(books_to_show,
                           df_name = "books",
                           df_fields = ['title', 'author'],
                           df_title = "Please select books to remove from favorites",
                           df_search_term="IDs",
                           use_search = True
                           )
        ids_to_remove_int = []
        print(self.favorites)
        print(ids_to_remove)
        for i in ids_to_remove:
            ids_to_remove_int.append(int(i))
        final_st = set(self.favorites).difference(set(ids_to_remove_int))
        self.favorites = []
        for i in final_st:
            self.favorites.append(i)
        self.auther.userdb.edit_user_in_dataframe(self)
        
    def write_a_review(self):
        if self.orders == []:
            print("Orders empty, you can't write a review.")
            return
        orders = self.auther.librarydb.get_orders_by_user_id(self.ID)
        print("The ordered books:")
        ordered_books = self.auther.librarydb.books_df.loc[orders['book_id']]
        print(ordered_books['title'])
        print("Please type the ID for the review")
        inp = input()
        inp = int(inp)
        print("Please rate from 1-10")
        rating = input()
        rating = int(rating)
        if rating < 1 or rating > 10:
            print("Invalid range")
            rating = -1
        print("Please write the review (leave empty for no review)")
        review = input()
        if not review == "" and rating > 0:
            self.auther.librarydb.add_review({'book_id' : inp,
                                            'user_id' : self.ID,
                                            'rating' : rating,
                                            'contents' : review})
    
    def add_books_to_favorites_csv(self):
        print("Please type the path of the csv of the books you would like to add.")
        inp = input()
        book_tmp = pd.DataFrame(self.auther.librarydb.books_df)
        imported_df = pd.read_csv(inp).astype('object')
        def to_int_list(lis):
            if not pd.isna(lis):
                return ast.literal_eval(lis)
            return []
        self.imported_df['categories'] = self.imported_df['categories'].apply(to_int_list)
        self.imported_df['bookstores'] = self.imported_df['bookstores'].apply(to_int_list)
        # final_imported_df = imported_df
        for index, row in imported_df.iterrows():
            if not self.auther.librarydb.check_if_book_real(row['title'], row['author'], row['publisher'], row['categories']):
                # final_imported_df = final_imported_df.drop(index = index)
                self.favorites.append(self.auther.librarydb.add_custom_book(row['title'], row['author'], row['publisher'], row['categories'], self.ID))
            else:
                book_tmp = book_tmp.loc[book_tmp['title'] == row['title']]
                book_tmp = book_tmp.loc[book_tmp['author'] == row['author']]
                book_tmp = book_tmp.loc[book_tmp['publisher'] == row['publisher']]
                book_tmp = book_tmp.loc[book_tmp['categories'] == row['categories']]
                
        fave_set = set(self.favorites)
        
        # for i in list(final_imported_df.index):
        #     fave_set.add(i)
        for i in list(book_tmp.index):
            fave_set.add(i)
        self.favorites = list(fave_set)
        self.auther.userdb.edit_user_in_dataframe(self)
        

    def browse_favorite_books(self):
        real_favorites = []
        fake_favorites = []
        for i in self.favorites:
            if i > 0:
                real_favorites.append(i)
        books_to_show = self.auther.librarydb.books_df.loc[real_favorites]
        fake_books_to_show = self.auther.librarydb.get_custom_book_by_user_id(self.ID)
        fake_books_to_show = fake_books_to_show.drop(labels = 'user_id', axis = 1 )
        books_to_show = pd.concat([books_to_show,fake_books_to_show])
        if self.favorites == []:
            print("No favorite books exist")
            return
        def trigg(boolean):
            if boolean:
                return "Is Availiable"
            else:
                return "Is not Availiable"
        books_to_show['availiability'] = books_to_show['availiability'].apply(trigg)
        def trigg2(number):
            return f"{number}$"
        books_to_show['cost'] = books_to_show['cost'].apply(trigg2)
        book_outp = bo.print_dataframe(books_to_show,
                           df_name = "books",
                           df_fields = ['title', 'cost', 'availiability'],
                           use_search = True,
                           multiple = True,
                           df_title = "Favorite books availiability and cost.",
                           df_search_term = "Book IDs"
                           )
        if book_outp == []:
            print("Plain enter is invalid input.")
            return
        book_outp_int = []
        for i in book_outp:
            if not int(i) in list(books_to_show.index):
                print("Excluding id " + i)
            else:
                book_outp_int.append(int(i))
        if books_to_show.loc[book_outp_int].empty:
            print("No books found availiable from the selected ones.")
        else:
            print("Below is the availiability and price for the selected books.")
            print(books_to_show.loc[book_outp_int][['title', 'cost', 'availiability']])
    
    def export_as_list(self):
        return [ self.ID,
                self.username,
                self.password,
                self.address,
                self.city,
                self.orders,
                self.favorites,
                self.balance]
    
    def import_from_df(self, df):
        self.ID = df.index.values[0]
        self.username = df.loc[self.ID, "username"]
        self.password = df.loc[self.ID, "password"]
        self.address = df.loc[self.ID, "address"]
        self.city = df.loc[self.ID, "city"]
        self.orders = df.loc[self.ID, "orders"]
        self.favorites = df.loc[self.ID, "favorites"]
        self.balance = df.loc[self.ID, 'balance']
    
    def import_from_dict(self, dictionary):
        self.username = dictionary["username"]
        self.password = dictionary[ "password"]
        self.address = dictionary[ "address"]
        self.city = dictionary[ "city"]
        self.orders = dictionary[ "orders"]
        self.favorites = dictionary[ "favorites"]
        self.balance = df.loc[self.ID, 'balance']

class Admin():
    def __init__(self, ID = -1, username="Oh", password="Hello", bookstores=["There"]):
        self.ID = ID
        self.username = username
        self.password = password
        self.bookstores = bookstores
        self.auther = None
    
    def set_auther(self, auther):
        self.auther = auther
    
    def make_statistics(self):
        # self.auther.librarydb.
        # self.auther.userdb.
        # ab = self.auther.librarydb.get_all_bookstores()
        # aa = self.auther.librarydb.get_all_authors()
        # ap = self.auther.librarydb.get_all_publishers()
        # ur = self.auther.userdb.get_all_cities()
        ana , anna = self.auther.librarydb.get_num_books_by_author()
        anb, annb = self.auther.librarydb.get_num_books_by_bookstores()
        anp, annp = self.auther.librarydb.get_num_books_by_publisher()
        dist = self.auther.librarydb.get_distribution_by_avail_books()
        distb = self.auther.librarydb.books_df.index.values
        ura,  ucity = self.auther.userdb.get_num_users_by_city()
        
        
        bo.make_bar_graph(anb, "Bookstores", "Number of books", "Number of books per bookstore")
        bo.make_bar_graph(annb, "Bookstores", "Number of books", "Number of books per bookstore (copies included)")
        bo.make_bar_graph(ana, "Authors", "Number of books", "Number of books per author")
        bo.make_bar_graph(anna, "Authors", "Number of books", "Number of books per author (copies included)")
        bo.make_bar_graph(anp, "Publishers", "Number of books", "Number of books per publisher")
        bo.make_bar_graph(annp, "Publishers", "Number of books", "Number of books per publisher (copies included)")
        bo.make_bar_graph(dist, "Distribution", "Number of books", "Number of books per bookstore")
        bo.make_bar_graph(ura, "Cities", "Number of users", "Number of users per city")
    
    def add_book(self):
        book = blm.Book()
        print("Please enter bookstore to be added:")
        num = 1
        for i in self.bookstores:
            print(f"{num} : {i}")
            num = num + 1
        inp = input()
        inp = inp.split(',')
        bk=[]
        vals = []
        for i in inp:
            print(self.bookstores)
            bk.append(self.bookstores[int(i)-1])
            vals.append(0)
        dk = dict(zip(bk,vals))
        print("Please edit the values for the book to be inserted")
        # base = {'ID' : -1,
        # 'title' : "Test",
        # 'author' : "Test",
        # 'publisher' : "Test",
        # 'categories' : ["fiction"],
        # 'cost' : 0.0,
        # 'shipping_cost' : 0.0,
        # 'availiability' : False,
        # 'copies' : 0,
        # 'bookstores' : dk}
        # base = bo.dict_editor_custom(base, ['title', 'authors', 'publisher', 'categories', 'cost', 'shipping_cost', 'availiability', 'copies'])
        # base['title'] = input("Enter the title: ")
        book.title = input("Enter the title: ")
        # base['author'] = input("Enter the name of the author: ")
        book.author = input("Enter the name of the author: ")
        # base['publisher'] = input("Enter the name of the publisher: ")
        book.publisher = input("Enter the name of the publisher: ")
        print("Is this book informational or literature?(1/2)")
        inp = input()
        if inp == "1":
            # base['categories'] = ['informational']
            book.categories = ['informational']
            print("Add additional categories:")
            categories_ed = ["mathematics", "history", "computer-science", "physics", "cooking", "biography"]
            num = 1
            for i in categories_ed:
                print(f"({num}) {i}")
                num = num + 1
            inp = int(input()) -1
            # base['categories'].append(categories_ed[inp])
            book.categories.append(categories_ed[inp])
        else:
            # base['categories'] = ['literature']
            book.categories = ['literature']
            print("Add additional categories:")
            categories_lit = ["fantasy", "adventure", "sci-fi", "mystery", "comic"]
            num = 1
            for i in categories_lit:
                print(f"({num}) {i}")
                num = num + 1
            inp = int(input()) -1
            # base['categories'].append(categories_lit[inp])
            book.categories.append(categories_lit[inp])
        # base['cost'] = float(input("Enter the cost of the book: "))
        book.cost = float(input("Enter the cost of the book: "))
        # base['shipping_cost'] = float(input("Enter the shipping cost of the book: "))
        book.shipping_cost = float(input("Enter the shipping cost of the book: "))
        inp = input("Is this book availiable?[Y/n]:")
        if inp == "Y":
            # base['availiability'] = True
            book.availiability = True
        else:
            # base['availiability'] = False
            book.availiability = False
        copies_per_bks = {}
        for i in dk:
            # base['bookstores'][i]=input(f"How many copies are in {i}? : ")
            copies_per_bks[i]=int(input(f"How many copies are in {i}? : ") )
        book.bookstores = copies_per_bks
        # book.import_from_dict(base)
        self.auther.librarydb.add_book(book)
        
        
    def import_books_df(self):
        print("Please type the path of the csv of the books you would like to add.")
        inp = input()
        self.auther.librarydb.import_new_books(inp)
        
    def edit_book(self):
        books = self.auther.get_avail_books_for_del()
        books_to_edit = bo.print_dataframe( df = books,
                                            df_name = "books",
                                            df_fields = ["title", "author"],
                                            df_title = "Please search the books you would like to edit.",
                                            use_search = True,
                                            df_search_term = "title",
                                            interval = 10
                                            )
        if books_to_edit == []:
            return
        final_books = pd.DataFrame(columns=books.columns)
        for i in books_to_edit:
            final_books = pd.concat([blm.get_books_by_name_with_df(books, i), final_books])
        
        if final_books.shape[0] > 1:
            book_to_edit = bo.print_dataframe(  df = final_books,
                                                df_name = "book",
                                                df_fields = ["title", "author"],
                                                df_title = "Please select the ID of the book you would like to edit.",
                                                use_search = True,
                                                df_search_term = "ID",
                                                interval = 10,
                                                multiple = False
                                                )
            if books_to_edit == []:
                return
            book_to_edit = int(book_to_edit)
        if not set(final_books.index.values).issuperset(set([book_to_edit])):
            print("Invalid Index. Please try again.")
        else:
            book = self.auther.librarydb.get_book_at_index(book_to_edit)
            print("You are now editing the below book.")
            book.print_me()
            
            book = blm.Book()
            print("Please enter bookstore to be added:")
            num = 1
            for i in self.bookstores:
                print(f"{num} : {i}")
                num = num + 1
            inp = input()
            inp = inp.split(',')
            bk=[]
            vals = []
            for i in inp:
                print(self.bookstores)
                bk.append(self.bookstores[int(i)-1])
                vals.append(0)
            dk = dict(zip(bk,vals))
            print("Please edit the values for the book to be inserted")
            # base = {'ID' : -1,
            # 'title' : "Test",
            # 'author' : "Test",
            # 'publisher' : "Test",
            # 'categories' : ["fiction"],
            # 'cost' : 0.0,
            # 'shipping_cost' : 0.0,
            # 'availiability' : False,
            # 'copies' : 0,
            # 'bookstores' : dk}
            # base = bo.dict_editor_custom(base, ['title', 'authors', 'publisher', 'categories', 'cost', 'shipping_cost', 'availiability', 'copies'])
            # base['title'] = input("Enter the title: ")
            book.title = input("Enter the title: ")
            # base['author'] = input("Enter the name of the author: ")
            book.author = input("Enter the name of the author: ")
            # base['publisher'] = input("Enter the name of the publisher: ")
            book.publisher = input("Enter the name of the publisher: ")
            print("Is this book informational or literature?(1/2)")
            inp = input()
            if inp == "1":
                # base['categories'] = ['informational']
                book.categories = ['informational']
                print("Add additional categories:")
                categories_ed = ["mathematics", "history", "computer-science", "physics", "cooking", "biography"]
                num = 1
                for i in categories_ed:
                    print(f"({num}) {i}")
                    num = num + 1
                inp = int(input()) -1
                # base['categories'].append(categories_ed[inp])
                book.categories.append(categories_ed[inp])
            else:
                # base['categories'] = ['literature']
                book.categories = ['literature']
                print("Add additional categories:")
                categories_lit = ["fantasy", "adventure", "sci-fi", "mystery", "comic"]
                num = 1
                for i in categories_lit:
                    print(f"({num}) {i}")
                    num = num + 1
                inp = int(input()) -1
                # base['categories'].append(categories_lit[inp])
                book.categories.append(categories_lit[inp])
            # base['cost'] = float(input("Enter the cost of the book: "))
            book.cost = float(input("Enter the cost of the book: "))
            # base['shipping_cost'] = float(input("Enter the shipping cost of the book: "))
            book.shipping_cost = float(input("Enter the shipping cost of the book: "))
            inp = input("Is this book availiable?[Y/n]:")
            if inp == "Y":
                # base['availiability'] = True
                book.availiability = True
            else:
                # base['availiability'] = False
                book.availiability = False
            copies_per_bks = {}
            for i in dk:
                # base['bookstores'][i]=input(f"How many copies are in {i}? : ")
                copies_per_bks[i]=int(input(f"How many copies are in {i}? : ") )
            book.bookstores = copies_per_bks
                # dc = bo.dict_editor( self.auther.librarydb.get_book_as_dict(book.ID) )
                # dc["ID"] = book.ID
                # book = blm.Book()
                # book.import_from_dict(dc)
                # edited_book = book
            self.auther.librarydb.edit_book(book)
            self.auther.librarydb.fix_copies(book.ID)
    
    def check_book_avail(self):
        books = self.auther.librarydb.books_df
        print("Would you like to specify bookstores?[Y/n]")
        inp = input()
        if inp == "Y":
            print("Please specify the bookstores (comma separated)")
            inp = input()
            inp = inp.split(',')
            dict_books = self.auther.librarydb.get_books_by_bookstores(inp)
            books = pd.concat(list(dict_books.values()), axis = 0)
        books_to_chk = bo.print_dataframe(  df = books,
                                            df_name = "books",
                                            df_fields = ["title", "author"],
                                            df_title = "Please search the books you would like to check the availiability for.",
                                            use_search = True,
                                            df_search_term = "title",
                                            interval = 10
                                            )
        if books_to_chk == "":
            return
        final_books = pd.DataFrame(columns=books.columns)
        for i in books_to_chk:
            final_books = pd.concat([blm.get_books_by_name_with_df(books, i), final_books])
        if final_books.shape[0] > 1:
            books_to_chk = bo.print_dataframe(  df = final_books,
                                                df_name = "books",
                                                df_fields = ["title", "author"],
                                                df_title = "Please search the IDs of the books you would like to check the availiability for.",
                                                use_search = True,
                                                df_search_term = "IDs",
                                                interval = 10
                                                )
            if books_to_chk == "":
                return
            books_to_chk_int = []
            for i in books_to_chk:
                books_to_chk_int.append(int(i))
            if not set(final_books.index.values).issuperset(set(books_to_chk_int)):
                print("Invalid index. Please try again.")
            else:
                books_to_show = final_books.loc[books_to_chk_int]
                # books_to_show = pd.DataFrame(columns=final_books.columns)
                # for i in books_to_chk_int:
                #     books_to_show = pd.concat([final_books.loc[i], books_to_show])
        else:
            books_to_show = final_books.loc[int(i)].copy()
        def trigg(boolean):
            if boolean:
                return "Is Availiable"
            else:
                return "Is not Availiable"
        books_to_show['availiability'] = books_to_show['availiability'].apply(trigg)
        print(books_to_show[['title','availiability']])
        # bo.print_dataframe(books_to_show, df_name = "books", df_fields = ['title','availiability'])

    def delete_books(self):
        books = self.auther.get_avail_books_for_del()
        print(books)
        books_to_del = bo.print_dataframe(  df = books,
                                            df_name = "books",
                                            df_fields = [ "title", "author" ],
                                            df_title = "Please search the books you would like to delete.",
                                            use_search = True,
                                            df_search_term = "title",
                                            interval = 10
                                            )
        if books_to_del == "":
            return
        final_books = pd.DataFrame(columns=books.columns)
        for i in books_to_del:
            final_books = pd.concat([blm.get_books_by_name_with_df(books, i), final_books])
        if final_books.shape[0] > 1:
            books_to_del = bo.print_dataframe(  df = final_books,
                                                df_name = "books",
                                                df_fields = ["title", "author"],
                                                df_title = "Please search the IDs of the books you would like to delete.",
                                                use_search = True,
                                                df_search_term = "IDs",
                                                interval = 10
                                                )
            if books_to_del == "":
                print("Invalid Input.")
                return
            books_to_del_int = []
            for i in books_to_del:
                books_to_del_int.append(int(i))
            if not set(final_books.index.values).issuperset(set(books_to_del_int)):
                print("Invalid index. Please try again.")
            else:
                for i in books_to_del_int:
                    self.auther.librarydb.remove_book_with_ID(i)
        else:
            self.auther.librarydb.remove_book_with_ID(final_books.index.values[0])
        
        
            

    def export_books_df(self):
        print("Please insert the path to export.")
        inp = input()
        self.auther.librarydb.save_to_path(inp)
    
    def delete_reviews(self):
        books = self.auther.get_avail_books_for_del()
        print(books)
        books_to_del = bo.print_dataframe(  df = books,
                                            df_name = "books",
                                            df_fields = [ "title", "author" ],
                                            df_title = "Please search the book you would like to delete reviews of.",
                                            use_search = True,
                                            df_search_term = "title",
                                            interval = 10
                                            )
        if books_to_del == "":
            return
        final_books = pd.DataFrame(columns=books.columns)
        for i in books_to_del:
            final_books = pd.concat([blm.get_books_by_name_with_df(books, i), final_books])
        books_to_del_int = []
        if final_books.shape[0] > 1:
            books_to_del = bo.print_dataframe(  df = final_books,
                                                df_name = "books",
                                                df_fields = ["title", "author"],
                                                df_title = "Please search the ID of the book you would like to delete reviews.",
                                                use_search = True,
                                                df_search_term = "ID",
                                                interval = 10
                                                )
            if books_to_del == "":
                return
            for i in books_to_del:
                books_to_del_int.append(int(i))
            if not set(final_books.index.values).issuperset(set(books_to_del_int)):
                print("Invalid index. Please try again.")
                return 
        else:
            books_to_del_int.append(final_books.index.values[0])
        final_reviews = pd.DataFrame(columns=self.auther.librarydb.reviews_df.columns)
        for i in books_to_del_int:
            final_reviews = pd.concat([self.auther.librarydb.reviews_df.loc[self.auther.librarydb.reviews_df["book_id"] == i], final_reviews])
            if final_reviews.empty:
                print("This book has no reviews")
                continue
            reviews_to_del = bo.print_dataframe(  df = final_reviews,
                                                df_name = "reviews",
                                                df_fields = ["rating", "contents", "user_id"],
                                                df_title = "Please search the IDs of the reviews you would like to delete.",
                                                use_search = True,
                                                df_search_term = "IDs",
                                                interval = 10
                                                )
            reviews_to_del_int = []
            for i in reviews_to_del:
                reviews_to_del_int.append(int(i))
                
            for i in reviews_to_del_int:
                print("Would you like to delete the whole review?")
                inp = input()
                if inp == "Y":
                    self.auther.librarydb.remove_review_with_ID(i)
                    print(f"Deleted review with id {i}")
                else:
                    temp = dict(self.auther.librarydb.reviews_df.loc[i])
                    temp['contents'] = ''
                    self.auther.librarydb.reviews_df.loc[i] = temp
            # self.auther.librarydb.remove_book_with_ID(i)
    
    def delete_user(self):
        users = self.auther.userdb.user_df
        user_to_del = bo.print_dataframe(  df = users,
                                            df_name = "users",
                                            df_fields = ["username", "city"],
                                            df_title = "Please search the users you would like to delete.",
                                            use_search = True,
                                            df_search_term = "username",
                                            interval = 10,
                                            multiple = False
                                            )
        if not user_to_del == "":
            final_users = get_users_by_name_with_df(users, user_to_del)
            if final_users.shape[0] > 1:
                user_to_del = bo.print_dataframe(  df = final_users,
                                                    df_name = "users",
                                                    df_fields = ["username", "city"],
                                                    df_title = "Please search the IDs of the users you would like to delete.",
                                                    use_search = True,
                                                    df_search_term = "IDs",
                                                    interval = 10
                                                    )
                users_to_del_int = []
                for i in user_to_del:
                    users_to_del_int.append(int(i))
                if not set(final_users.index.values).issuperset(set(users_to_del_int)):
                    print("Invalid index. Please try again.")
                else:
                    for i in users_to_del_int:
                        self.auther.userdb.remove_user_from_dataframe_ID(i)
            else:
                self.auther.userdb.remove_user_from_dataframe_ID(final_users.index.values[0])

    def check_book_cost(self):
        books_to_show = self.auther.librarydb.books_df
        books_to_show['total_cost'] = books_to_show['cost'] + books_to_show['shipping_cost']
        def trigg2(number):
            return f"{number}$"
        books_to_show['total_cost'].apply(trigg2)
        outp = bo.print_dataframe(books_to_show, df_search_term="IDs", df_name = "books", df_fields = ['title', 'total_cost'], use_search = True, df_title = "Please search for the books you want to check.")
        outp_int = []
        for i in outp:
            outp_int.append(int(i))
        bo.print_dataframe(books_to_show.loc[outp_int], df_search_term="IDs", df_name = "books", df_fields = ['title', 'total_cost'], df_title = "These are the specific books")

    def check_total_book_cost(self):
        auth = self.auther.librarydb.get_all_authors()
        pub = self.auther.librarydb.get_all_publishers()
        for i in pub:
            a,b = self.auther.librarydb.get_cost_books_by_publisher(i)
            print(f"Total cost per publisher {i}:{a}")
            print(f"Total cost per publisher {i} (per_copy):{b}")
        for i in auth:
            a,b = self.auther.librarydb.get_cost_books_by_author(i)
            print(f"Total cost per author {i}:{a}")
            print(f"Total cost per author {i} (per_copy):{b}")
        a, b =self.auther.librarydb.get_cost_books()
        print(f"Total cost all books:{a}")
        print(f"Total cost all books (per_copy):{b}")

    def export_as_list(self):
        return [ self.ID, self.username, self.password, self.bookstores]
    
    def import_from_df(self, df):
        # print(df)
        self.ID = df.index.values[0]
        self.username = df.loc[self.ID, "username"]
        self.password = df.loc[self.ID, "password"]
        self.bookstores = df.loc[self.ID, "bookstores"]
    

def get_users_by_name_with_df(df, string):
    return df.loc[df["username"].str.contains(string, case=False)]
    
