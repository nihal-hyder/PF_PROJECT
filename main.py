import random


SPECIAL_CHARACTER = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', '.', '/',
    ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
]
UPPER_CASE_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER_CASE_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
MIN_LENGTH = 8
MAX_ATTEMPTS = 3
USERS_FILE = "user.txt"
LOG_FILE = "log.txt"


def welcome_interface():
    print("\nwelcome to the system\n what do you want to do ?")
    print(" 1. Register a new user")
    print(" 2. Login")
    print(" 3. Generate a strong password")
    print(" 4. Exit")
    


def check_password_strength(password):
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        if char in UPPER_CASE_LETTERS:
            has_upper = True
        elif char in LOWER_CASE_LETTERS:
            has_lower = True
        elif char in DIGITS:
            has_digit = True
        elif char in SPECIAL_CHARACTER:
            has_special = True

    score = 0
    if len(password) >= MIN_LENGTH:
        score += 1
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1

    if score == 5:
        rating = "Strong"
    elif score >= 3:
        rating = "Medium"
    else:
        rating = "Weak"

    return score, rating


def password_tips(password):
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        if char in UPPER_CASE_LETTERS:
            has_upper = True
        elif char in LOWER_CASE_LETTERS:
            has_lower = True
        elif char in DIGITS:
            has_digit = True
        elif char in SPECIAL_CHARACTER:
            has_special = True

    print("your password needs:")
    if len(password) < MIN_LENGTH:
        print(f" - at least {MIN_LENGTH} characters")
    if not has_upper:
        print(" - an uppercase letter (A-Z)")
    if not has_lower:
        print(" - a lowercase letter (a-z)")
    if not has_digit:
        print(" - a digit (0-9)")
    if not has_special:
        print(" - a special character (like ! @ # $)")


def generate_password(length=12):
    if length < MIN_LENGTH:
        length = MIN_LENGTH

    password_pool = [
        random.choice(SPECIAL_CHARACTER),
        random.choice(UPPER_CASE_LETTERS),
        random.choice(DIGITS),
        random.choice(LOWER_CASE_LETTERS)
    ]

    all_characters = SPECIAL_CHARACTER + list(UPPER_CASE_LETTERS) + list(LOWER_CASE_LETTERS) + list(DIGITS)

    remaining_length = length - len(password_pool)
    for i in range(remaining_length):
        password_pool.append(random.choice(all_characters))

    random.shuffle(password_pool)

    strong_password = ""
    for char in password_pool:
        strong_password += char
    return strong_password


def write_log(username, result):
    with open(LOG_FILE, "a") as f:
        f.write(f"{username},{result}\n")


def check_username(username):
    try:
        with open(USERS_FILE, "r") as f:
            for user in f:
                part = user.strip().split(',')
                if part[0] == username:
                    return False
        return True
    except FileNotFoundError:
        return True


def get_password(username):
    try:
        with open(USERS_FILE, "r") as f:
            for line in f:
                content = line.strip().split(',')
                if len(content) == 2 and content[0] == username:
                    return content[1]
    except FileNotFoundError:
        pass
    return None


def register_new_user():
    print("\n--- Register a new user ---")

    while True:
        username = input("enter your username here: ").strip()
        if username == "":
            print("username cannot be empty")
        elif ',' in username or ' ' in username:
            print("username cannot contain a comma or a space")
        elif not check_username(username):
            print(f"user : {username} already exists")
        else:
            break

    print(f"suggested password is {generate_password()}")

    while True:
        password = input("enter your password here: ")
        if ',' in password or ' ' in password:
            print("password cannot contain a comma or a space")
            continue

        score, rating = check_password_strength(password)
        print(f"password strength: {rating} ({score}/5)")

        if rating != "Strong":
            password_tips(password)
            print("please try again")
            continue

        confirm = input("confirm your password: ")
        if confirm != password:
            print("passwords do not match, try again")
            continue
        break

    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password}\n")
    print(f"user {username} is successfully saved!")


def login():
    print("\n--- Login ---")
    username = input("enter your username here: ").strip()

    if username == "":
        print("enter a username")
        return False

    saved_password = get_password(username)
    if saved_password is None:
        print("username does not exist!")
        write_log(username, "FAILED")
        return False

    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        password = input(f"enter your password here (attempt {attempt}/{MAX_ATTEMPTS}): ")
        if password == saved_password:
            print("login successful!")
            write_log(username, "SUCCESS")
            return True
        else:
            write_log(username, "FAILED")
            print(f"wrong password! {MAX_ATTEMPTS - attempt} attempt(s) left")
        attempt += 1

    print("too many failed attempts. account locked!")
    return False


def password_generator_menu():
    print("\n--- Generate a strong password ---")
    while True:
        try:
            length = int(input(f"enter password length ({MIN_LENGTH}-32): "))
        except ValueError:
            print("please enter a whole number")
            continue

        if length < MIN_LENGTH or length > 32:
            print(f"length must be between {MIN_LENGTH} and 32")
        else:
            break

    password = generate_password(length)
    score, rating = check_password_strength(password)
    print(f"your strong password is {password}")
    print(f"strength: {rating} ({score}/5)")


def main():
    try:
        while True:
            welcome_interface()
            try:
                choice = int(input("Choose an option (1-4): "))
            except ValueError:
                print("please enter a number")
                continue

            if choice == 1:
                register_new_user()
            elif choice == 2:
                login()
            elif choice == 3:
                password_generator_menu()
            elif choice == 4:
                break
            else:
                print("please choose a number from 1 to 4")
    finally:
        print("all data is saved. goodbye!")


main()