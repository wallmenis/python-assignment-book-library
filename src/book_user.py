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
            
        self.user_df = self.user_df.set_index("ID")
        self.admin_df = self.admin_df.set_index("ID")
        
    def add_admin_to_dataframe(self, admin):
        tmp_admin = admin.Copy()
        tmp_admin.ID = self.admin_df.loc[admin_df.shape[0]] + 1
        self.admin_df = pd.concat(pd.DataFrame(admin.export_as_list()) columns = self.admin_df.columns, self.admin_df)

    def add_user_to_dataframe(self, user):
        tmp_user = user.Copy()
        tmp_user.ID = self.user_df.loc[admin_df.shape[0]] + 1
        self.user_df = pd.concat(pd.DataFrame(user.export_as_list()) columns = self.user_df.columns, self.user_df)
    
    def remove_admin_from_dataframe(self, admin):
        self.admin_df.drop(index = admin.ID)
    
    def remove_user_from_dataframe(self, user):
        self.user_df.drop(index = user.ID)
    
    def edit_user_in_dataframe(self, user):
        self.user_df.loc[user.ID] = user.export_as_list()
    
    def edit_admin_in_dataframe(self, admin):
        self.admin_df.loc[admin.ID] = admin.export_as_list()


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