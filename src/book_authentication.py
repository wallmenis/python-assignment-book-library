import book_user as bu
import book_library_management as blm
import re

class Authenticator():
    def __init__(self):
        self.userdb=bu.UserDB()
        self.librarydb=blm.LibraryDB()
        self.currentUser = None

    def login(self ,username, password):
        print("placeholder")


    def register_user(self):
        print("placeholder")


    def start_procedure(self):
        if userdb.admin_df.empty:
            print("No registered admin found. Please register a new admin.")
            register_user()


def validate_password(password):
    output = 0
    if len(password) > 7:
        output += 1
    if not re.match("[$&+,:;=?@#|'<>.^*()%!-]", password):
        output += 2
    return output

