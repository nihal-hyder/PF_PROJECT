import random


SPECIAL_CHARACTER = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
]
UPPER_CASE_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER_CASE_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
MAX_FAILED = 3
LOG_FILE = "log.txt"


def welcome_interface():
    print('\nwelcome to the system\n what do you want to do ?')
    print(" 1. Register a new user\n 2. Login\n 3. Generate a strong password\n 4. View security report\n 5. Exit")
    print("Choose an option (1-5):")


def check_password_strenght(password):
    if len(password) >= 8 and any(char in SPECIAL_CHARACTER for char in password) and any(char in DIGITS for char in password ) and any(char in UPPER_CASE_LETTERS for char in password ) :
        return True
    else:
        return False


def generating_strong_password(length=12):
    if length < 8:
        length = 8

    password_pool = [
        random.choice(SPECIAL_CHARACTER),
        random.choice(UPPER_CASE_LETTERS),
        random.choice(DIGITS),
        random.choice(LOWER_CASE_LETTERS)
    ]

    all_characters = SPECIAL_CHARACTER + list(UPPER_CASE_LETTERS) + list(LOWER_CASE_LETTERS) + list(DIGITS)
    all_characters.remove(',')

    remaining_length = length - len(password_pool)
    password_pool += random.choices(all_characters, k=remaining_length)

    random.shuffle(password_pool)

    strong_password = ''.join(password_pool)
    if ',' in strong_password:
        return generating_strong_password(length)
    return strong_password


def write_log(username, result):
    with open(LOG_FILE, "a") as f:
        f.write(f"{username},{result}\n")


def login():
    username = input("enter your username here: ")
    password = input("enter your password here: ")
    if username and password :
        try:
            with open("user.txt" ,"r") as f:
                for line in f:
                    content = line.strip().split(',')
                    if len(content) == 2 and content[0] == username and content[1] == password:
                        print("login succesfull !")
                        write_log(username, "SUCCESS")
                        return True
        except FileNotFoundError:
            pass
        print("username or password is wrong !")
        write_log(username, "FAILED")
        return False
    else:
        print("enter an username and password")
        return False


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
            return True


def register_new_user():
    username = input("enter your username here: ")
    if username == "" or ',' in username:
        print("username cannot be empty or contain a comma")
        return
    if not checking_username(username):
        return

    print(f"suggest password is {generating_strong_password()}")
    password = input("enter your password here: ")

    if ',' in password:
        print("password cannot contain a comma")
    elif check_password_strenght(password) :
            with open("user.txt", "a") as f :
                f.write(f"{username},{password}\n")
            print(f"user {username} is succesfully saved! ")
    else:
                print("soory password is not enough strong")


def load_log():
    records = []
    try:
        with open(LOG_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split(",")
                if len(parts) == 2:
                    records.append((parts[0], parts[1]))
    except FileNotFoundError:
        print("No log file found yet. Try logging in first.")
    return records


def show_report():
    print("\n========== SECURITY REPORT ==========")

    records = load_log()
    if len(records) == 0:
        print("No login data to report.")
        return

    failed = {}
    success = {}
    all_names = set()

    for name, result in records:
        all_names.add(name)
        if result == "FAILED":
            failed[name] = failed.get(name, 0) + 1
        else:
            success[name] = success.get(name, 0) + 1

    table = []
    for name in sorted(all_names):
        f = failed.get(name, 0)
        s = success.get(name, 0)
        total = f + s
        percent = f / total * 100

        if f >= MAX_FAILED:
            status = "SUSPICIOUS"
        else:
            status = "OK"

        table.append([name, s, f, total, f"{percent:.1f}%", status])

    headers = ["User", "Success", "Failed", "Total", "Fail %", "Status"]
    for h in headers:
        print(f"{h:<12}", end="")
    print()
    print("-" * 72)

    for row in table:
        for item in row:
            print(f"{str(item):<12}", end="")
        print()

    total_attempts = len(records)
    total_failed = 0
    for name in failed:
        total_failed += failed[name]

    print("\nTotal attempts :", total_attempts)
    print("Total failed   :", total_failed)
    print(f"Failure rate   : {total_failed / total_attempts * 100:.1f}%")

    pairs = []
    for name in failed:
        pairs.append((failed[name], name))
    pairs.sort(reverse=True)

    if len(pairs) > 0:
        print("\nTop targeted users:")
        rank = 1
        for count, name in pairs[:3]:
            print(f"  {rank}. {name} - {count} failed attempt(s)")
            rank += 1

    failed_names = set(failed.keys())
    success_names = set(success.keys())
    only_failed = failed_names - success_names

    if len(only_failed) > 0:
        print("\nNever logged in successfully (possible guessing attack):")
        for name in sorted(only_failed):
            print("   -", name)

    flagged = 0
    for row in table:
        if row[5] == "SUSPICIOUS":
            flagged += 1
    print(f"\nUsers flagged as SUSPICIOUS (>= {MAX_FAILED} failures): {flagged}")


def main():
    while True:
        welcome_interface()
        try:
            choice = int(input())
        except ValueError:
            print("please enter a number")
            continue

        if choice == 1:
            register_new_user()
        elif choice == 2:
            login()
        elif choice == 3:
            print(f"your strong password is {generating_strong_password()}")
        elif choice == 4:
            show_report()
        elif choice == 5:
            print("goodbye!")
            break
        else:
            print("please choose a number from 1 to 5")


main()