import re

class Validator:

    @staticmethod
    def password_check(password):
        # At least one lowercase, one uppercase, one digit, one special char, min 8 chars
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+!_]).{8,}$"
        return bool(re.fullmatch(pattern, password))

    @staticmethod
    def email_check(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.fullmatch(pattern, email))

    @staticmethod
    def usrname_check(usr_name):
        pattern = r"^[a-zA-Z]+\d+$"
        return bool(re.fullmatch(pattern, usr_name))

    @staticmethod
    def mobile_number_check(num):
        pattern = r"^[1-9][0-9]{9}$"
        return bool(re.fullmatch(pattern, str(num)))
