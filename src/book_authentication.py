import book_user as bu
import book_library_management as blm
import book_io as bo
import pandas as pd
import re

class Authenticator():
    def __init__(self):
        self.userdb=bu.UserDB()
        self.librarydb=blm.LibraryDB()
        self.currentUser = None

    def login(self):
        print("Please enter your username.")
        username = input()
        print("Please enter your password")
        self.currentUser = self.password_input(username)
        self.currentUser.set_auther(self)
    
    def password_input(self, username):
        failed = 0
        pusers = self.userdb.get_user_by_username(username)
        padmins = self.userdb.get_admin_by_username(username)
        # print(padmins)
        while failed < 3:
            inp = input()
            luser = pusers.loc[pusers['password'] == inp]
            ladmin = padmins.loc[padmins['password'] == inp]
            # print(ladmin)
            if luser.empty and ladmin.empty:
                failed = failed + 1
                print("Wrong password!!! Please try again.")
            else:
                if len(luser.index.values) > 1 or len(ladmin.index.values) > 1 :
                    print("DB_ERROR: USERS/ADMINS WITH SIMMILAR PASSWORD AND NAME FOUND")
                    print(f"PLEASE REPORT IDs {luser.index.values} AND {ladmin.index.values} TO AN ADMINISTRATOR TO RESOLVE THE ISSUE.")
                    exit(2)
                if len(luser.index.values) > 0:
                    us = bu.User()
                    us.import_from_df(luser)
                    return us
                ad = bu.Admin()
                ad.import_from_df(ladmin)
                return ad
        exit(1)
        return "You have failed pretty bad for this to be returned!"
            

    def register_admin(self):
        data_is_ok = False
        print("Do not worry for any mistakes; we will show you your information before confirming.")
        while(not data_is_ok):
            print("Please enter username for ADMIN account")
            username = input()
            password = password_register()
            print("Please enter the bookstores you will be administrating. Type exit to stop adding new ones.")
            bookstores = bo.input_list()
            print("Is the below data OK? Type YES if it is.")
            print(f"username: {username}")
            print(f"bookstores to administer: {bookstores}")
            inp = input()
            if re.match("YES", inp.replace(" ","")):
                data_is_ok = True
                if self.userdb.add_admin_to_dataframe(bu.Admin(-1, username, password, bookstores)):
                    print("Admin Added.")
                else:
                    data_is_ok = False
                    print("Admin with that username exists. Please use another username")

    def register_user(self):
        data_is_ok = False
        print("Do not worry for any mistakes; we will show you your information before confirming.")
        while(not data_is_ok):
            print("Please enter username for USER account")
            username = input()
            password = password_register()
            print("Please enter your home address.")
            address = input()
            print("Please enter the city in which you reside in.")
            city = input()
            print("Is the below data OK? Type YES if it is.")
            print(f"username: {username}")
            print(f"home address: {address}")
            print(f"city: {city}")
            inp = input()
            if re.match("YES", inp.replace(" ","")):
                data_is_ok = True
                if self.userdb.add_user_to_dataframe(bu.User(-1, username, password, address, city, [], [], 0.0)):
                    print("User Added.")
                else:
                    data_is_ok = False
                    print("User with that username exists. Please use another username")


    def start_procedure(self):
        if self.userdb.admin_df.empty:
            print("No registered admin found. Please register a new admin.")
            self.register_admin()
        print("Please choose.")
        print("1. Login")
        print("2. Register User")
        print("0. Exit")
        inp = input()
        if int(inp) == 1:
            self.login()
        elif int(inp) == 2:
            self.register_user()
            self.save_all()
            exit()
        else:
            exit()
        # print("2. Register User")
        
    
    def get_avail_books_for_del(self):
        # bk_per_bks = self.librarydb.get_books_by_bookstores(self.currentUser.bookstores)
        # return pd.concat(list(bk_per_bks.values()))
        # print(self.currentUser.bookstores)
        # return self.librarydb.get_books_by_bookstores(self.currentUser.bookstores)
        return self.librarydb.get_books_by_bookstores_exclusive(self.currentUser.bookstores)
    
    def order_book(self, index, bookstore):
        self.librarydb.order_book_with_index_from_bookstore(index,bookstore,self.currentUser.ID)
        
    def save_all(self):
        self.userdb.save_dataframes()
        self.librarydb.save_books_csv()
        self.librarydb.save_orders_csv()
        self.librarydb.save_reviews_csv()
        # self.librarydb.save_user_books_csv()

    def show_menu(self):
        print(f"Logged in as {self.currentUser.username}")
        if type(self.currentUser) == bu.Admin:
            print("User is Admin")
            print("(1) Add books.")
            print("(2) Remove books.")
            print("(3) Edit a book.")
            print("(4) Export book database data.")
            print("(5) Import book database data.")
            print("(6) Save current buffered data.")
            print("(7) Check book availiability.")
            print("(8) Check a book's total cost.")
            print("(9) Check book total cost.")
            print("(10) Delete a user.")
            print("(11) Get plots.")
            print("(12) Delete Review.")
            print("(0) Exit")
        else:
            print("User is regular")
            print("(1) Add favorite books.")
            print("(2) Add favorite books via csv.")
            print("(3) Remove favorite books.")
            print("(4) Modify personal information")
            print("(5) Check balance")
            print("(6) Check book price and availiability")
            print("(7) Order book.")
            print("(8) Return book.")
            print("(9) Check recommendations")
            print("(10) Write a review for an ordered book.")
            print("(0) Exit")
        print("Please select one of the options above.")
        
    def select_function(self):
        inp = input()
        inp = int(inp)
        if inp == 0:
                return True
        if type(self.currentUser) == bu.Admin:
            if inp == 1:
                self.currentUser.add_book()
            elif inp == 2:
                self.currentUser.delete_books()
            elif inp == 3:
                self.currentUser.edit_book()
            elif inp == 4:
                self.currentUser.export_books_df()
            elif inp == 5:
                self.currentUser.import_books_df()
            elif inp == 6:
                self.save_all()
            elif inp == 7:
                self.currentUser.check_book_avail()
            elif inp == 8:
                self.currentUser.check_book_cost()
            elif inp == 9:
                self.currentUser.check_total_book_cost()
            elif inp == 10:
                self.currentUser.delete_user()
            elif inp == 11:
                self.currentUser.make_statistics()
            elif inp == 12:
                self.currentUser.delete_reviews()
            else:
                print("Invalid option")
        else:
            if inp == 1:
                self.currentUser.add_books_to_favorites()
            elif inp == 2:
                self.currentUser.add_books_to_favorites_csv()
            elif inp == 3:
                self.currentUser.remove_books_from_favorites()
            elif inp == 4:
                self.currentUser.modify_account()
            elif inp == 5:
                self.currentUser.check_balance()
            elif inp == 6:
                # self.currentUser.check_book_avail()
                self.currentUser.browse_favorite_books()
            elif inp == 7:
                self.currentUser.order_book()
            elif inp == 8:
                self.currentUser.return_book()
            elif inp == 9:
                self.currentUser.show_recommendations()
            elif inp == 10:
                self.currentUser.write_a_review()
            else:
                print("Invalid option")
        return False

def password_register():    # We would preffer to return a salted hash but the assignment requires the password is stored in plain text
    password_is_ok = False  # This implementation helps us do this in the future since it detaches the rest of the codebase from the
    password = ""           # password registration part.
    while not password_is_ok:
        print("Please insert your new password.")
        print("Make sure it is at least eight(8) characters long and has at least one (1) non-numerical and non-letter character")
        password = input()
        valudation = validate_password(password)
        if valudation % 2 == 1:
            print("Password is not long enough.")
        if valudation > 1 :
            print("Password is missing non-numerical, non-letter character.")
        if valudation == 0:
            password_is_ok = True
        else:
            print("Please try again")
    return password

def validate_password(password):
    output = 0
    if len(password) < 8:
        output += 1
    if not len(re.sub("[^a-zA-Z0-9 ]", "", password)) > 0:
        output += 2
    return output
