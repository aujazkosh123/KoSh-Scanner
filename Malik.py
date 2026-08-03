import os, datetime
from colorama import Fore, Style, init
init(autoreset=True)

KEY_FILE = "keys.txt"
ADMIN_NUMBER = "923077321978"

BANNER = f"""{Fore.CYAN}
╔════════╗
║ {Fore.YELLOW} KoSh ADMIN CONTROL PANEL v1.0{Fore.CYAN} ║
║ {Fore.GREEN} Admin: {ADMIN_NUMBER}{Fore.CYAN} ║
╚════════╝{Style.RESET_ALL}
"""

def admin_login():
    num = input(Fore.GREEN + "Enter Admin WhatsApp Number: " + Style.RESET_ALL)
    if num!= ADMIN_NUMBER:
        print(Fore.RED + "❌ Access Denied. Only Admin" + Style.RESET_ALL)
        exit()
    print(Fore.GREEN + "✅ Admin Login Success" + Style.RESET_ALL)
    time.sleep(1)

def add_user():
    number = input("User WhatsApp Number 92xxxx: ")
    days = int(input("Kitne din ki key: "))
    expiry = datetime.datetime.now() + datetime.timedelta(days=days)

    with open(KEY_FILE, "a") as f:
        f.write(f"{number}|{expiry.strftime('%Y-%m-%d %H:%M:%S')}|ACTIVE\n")
    print(Fore.GREEN + f"✅ User Added! Expiry: {expiry.strftime('%Y-%m-%d %H:%M:%S')}" + Style.RESET_ALL)

def list_users():
    print(Fore.YELLOW + "\n[+] All Users" + Style.RESET_ALL)
    if not os.path.exists(KEY_FILE): print("Koi user nahi"); return
    with open(KEY_FILE) as f:
        for i, line in enumerate(f, 1):
            num, exp, status = line.strip().split("|")
            color = Fore.GREEN if status=="ACTIVE" else Fore.RED
            print(f"{i}. {color}{num} | {exp} | {status}{Style.RESET_ALL}")

def revoke_user():
    number = input("Kaunsa number revoke karna hai: ")
    lines = []
    with open(KEY_FILE) as f: lines = f.readlines()
    with open(KEY_FILE, "w") as f:
        for line in lines:
            if number in line:
                f.write(line.replace("ACTIVE", "REVOKED"))
            else:
                f.write(line)
    print(Fore.RED + "✅ User Revoked" + Style.RESET_ALL)

def extend_key():
    number = input("Kaunsa number extend karna hai: ")
    days = int(input("Kitne din aur: "))
    lines = []
    with open(KEY_FILE) as f: lines = f.readlines()
    with open(KEY_FILE, "w") as f:
        for line in lines:
            if number in line:
                num, exp, status = line.strip().split("|")
                new_exp = datetime.datetime.strptime(exp, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=days)
                f.write(f"{num}|{new_exp.strftime('%Y-%m-%d %H:%M:%S')}|{status}\n")
            else:
                f.write(line)
    print(Fore.GREEN + "✅ Expiry Extended" + Style.RESET_ALL)

def admin_panel():
    admin_login()
    while True:
        os.system("clear")
        print(BANNER)
        print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} New User Add karo")
        print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} All Users Dekho")
        print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} User Ko Revoke karo")
        print(f"{Fore.YELLOW}[4]{Style.RESET_ALL} Key Extend karo")
        print(f"{Fore.YELLOW}[5]{Style.RESET_ALL} Exit")
        ch = input(Fore.CYAN + "Select: " + Style.RESET_ALL)
        if ch == "1": add_user()
        elif ch == "2": list_users()
        elif ch == "3": revoke_user()
        elif ch == "4": extend_key()
        elif ch == "5": break
        input("\nEnter dabao...")

if __name__ == "__main__":
    import time
    admin_panel()
