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

    def register_admin(self):
        data_is_ok = False
        print("Do not worry for any mistakes; we will show you your information before confirming.")
        while(not data_is_ok):
            print("Please enter username for ADMIN account")
            username = input()
            password = password_register()

    def register_user(self):
        print("placeholder")


    def start_procedure(self):
        if userdb.admin_df.empty:
            print("No registered admin found. Please register a new admin.")
            register_admin()


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
    if len(password) > 7:
        output += 1
    if not re.match("[$&+,:;=?@#|'<>.^*()%!-]", password):
        output += 2
    return output

