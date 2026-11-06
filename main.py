import random


SPECIAL_CHARACTER = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', 
    ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
]
UPPER_CASE_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '0123456789'


def welcome_interface():
    print('welcome to the system\n what do you want to do ?0')
    print(" 1. Register a new user\n 2. Login\n 3. Generate a strong password\n 4. View security report\n 5. Show failed-login chart\n 6. Exit")
    print("Choose an option (1-6):")

welcome_interface()

def check_password_strenght(password):
    if len(password) >= 8 and any(char in SPECIAL_CHARACTER for char in password) and any(char in DIGITS for char in password ) and any(char in UPPER_CASE_LETTERS for char in password ) : #checking if the password has min of 8 letters
        return True
    else:
        return False


def generating_strong_password():
    pass

def login():
    username = input("enter your username here: ")
    password = input("enter your password here: ")
    if username and password :
        with open("user.txt" ,"r") as f:
           for line in f:
            content = line.strip().split(',')
            if content[0] == username and content[1] == password:
                    print("login succesfull !")
                    return True
            else:
                print("username or password is wrong !")
                return False
    else:
        print("enter an username and password")
        return False
    pass


def checking_username(username):
        try:
            with open("user.txt", "r") as f :
                for user in f :
                    part = user.strip().split(',')
                    if part[0] == username:
                        print(f"user : {username} already exits")
                        return False
            return True
        
        except FileNotFoundError:
            print('file not found')
            return True

        except:
            print("username already exists")

            return False

def register_new_user(username,password):

    
        
        if checking_username(username) :
            if check_password_strenght(password) :
                with open("user.txt", "a") as f :
                    f.write(f"{username},{password}\n")
                print(f"user {username} is succesfully saved! ")
            else:
                print("soory password is not enough strong")
        


def view_security_report():
    pass

def show_failed_login():
    pass
username = "nihalhydershah"
password =  "#Nihalhyder1212"

# register_new_user(username,password)

login()