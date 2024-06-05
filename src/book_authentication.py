import pandas as pd

class PrivilegeLevels(Enum):
    ADMIN = 0
    USER = 1
    UNAUTHENTICATED = 2

def validate_password(user, password):
    auth_level = PrivilegeLevels.UNAUTHENTICATED
    if user.password == password:
        auth_level = PrivilegeLevels.USER
    if user.isAdmin == True:
        auth_level = PrivilegeLevels.ADMIN
    return auth_level

def register_user()
