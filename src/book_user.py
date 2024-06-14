import pandas as pd
import book_authentication as ba

class UserDB():
    def __init__(self):
        self.user_df = pd.DataFrame({'ID' : [],
                                     'username' : [],
                                     'password' : [],
                                     'address' : [],
                                     'city' : [],
                                     'orders' : [],
                                     'favorites' : [],
                                     'balance' : []})
        self.admin_df = pd.DataFrame({'ID' : [],
                                      'username' : [],
                                      'password' : [],
                                      'bookstores' : []})
        try:
            self.user_df = pd.read_csv("../data/users.csv")
        except OSError:
            print("Failed to find/read books.csv file. Continuing with empty DataFrame")
        try:
            self.admin_df = pd.read_csv("../data/admins.csv")
        except OSError:
            print("Failed to find/read admins.csv file. Continuing with empty DataFrame")

    def add_admin_to_dataframe(self, admin):
        admin_df.iat[admin_df.shape[0]] = admin.export_as_list()

    def add_user_to_dataframe(self, user):
        user_df.iat[user_df.shape[0]] = user.export_as_list()



class User():
    def __init__(self,
                 ID=-1,
                 password="I",
                 username="Do",
                 address="Not",
                 city="Exist",
                 orders=["Here"],
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

    def export_as_list(self):
        return [ self.ID,
                self.password,
                self.username,
                self.address,
                self.city,
                self.orders,
                self.favorites,
                self.balance]

class Admin():
    def __init__(self, ID, password, username, bookstores):
        self.ID = ID
        self.password = password
        self.username = username
        self.bookstores = bookstores

    def export_as_list(self):
        return [ self.ID, self.password, self.username, self.bookstores]