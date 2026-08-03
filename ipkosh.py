import socket, concurrent.futures, datetime, time, ipaddress, sys, threading, os
from colorama import Fore, Style, init
init(autoreset=True)

KEY_FILE = "keys.txt"
MY_NUMBER = "923077321978" # Admin Number

def check_key():
    os.system("clear")
    print(Fore.CYAN + "╔══════════╗")
    print(Fore.YELLOW + "║ KoSh PREMIUM LOGIN ║")
    print(Fore.CYAN + "╚══════════╝" + Style.RESET_ALL)
    number = input(Fore.GREEN + "Enter WhatsApp Number 92xxxx: " + Style.RESET_ALL)

    if not os.path.exists(KEY_FILE):
        print(Fore.RED + "❌ Key system not found. Contact Admin" + Style.RESET_ALL)
        exit()

    with open(KEY_FILE) as f:
        for line in f:
            num, expiry, status = line.strip().split("|")
            if num == number and status == "ACTIVE":
                exp_time = datetime.datetime.strptime(expiry, '%Y-%m-%d %H:%M:%S')
                if datetime.datetime.now() < exp_time:
                    print(Fore.GREEN + f"✅ Access Granted | Expiry: {expiry}" + Style.RESET_ALL)
                    time.sleep(1)
                    return True
    print(Fore.RED + "❌ Invalid, Expired ya Revoked Key" + Style.RESET_ALL)
    exit()

check_key() # Login yahin hoga

socket.setdefaulttimeout(3)
DEFAULT_PAYLOAD = "GET / HTTP/1.1[crlf]Host: [host][crlf]Connection: close[crlf][crlf]"

BANNER = f"""{Fore.CYAN}
╔══════════╗
║ {Fore.YELLOW} WELCOME TO KoSh SCANNER v4.5 PREMIUM{Fore.CYAN} ║
║ {Fore.GREEN} Admin: {MY_NUMBER}{Fore.CYAN} ║
║ {Fore.GREEN} Save: 199,200,301,403,404,409,421{Fore.CYAN} ║
║ {Fore.RED} Developed = by Aijaz Kosh {Fore.CYAN} ║
╚══════════╝{Style.RESET_ALL}
"""

lock = threading.Lock()
sent = 0
live_count = 0
redirect_count = 0
allowed_codes = ["199","200","301","403","404","409","421"]
stats = {code:0 for code in allowed_codes}
stats["OTHER"] = 0
results_buffer = []

def resolve_domain(domain):
    try: return socket.gethostbyname(domain)
    except: return None

def generate_ips_from_cidr(cidr):
    network = ipaddress.ip_network(cidr, strict=False)
    return [str(ip) for ip in network.hosts()]

def scan_target(target, payload, port, is_domain=False):
    global sent, live_count, redirect_count
    ip = target; host_header = target
    if is_domain:
        ip = resolve_domain(target)
        if not ip:
            with lock: sent += 1
            return

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((ip, port))
        req = payload.replace("[host]", host_header).replace("[crlf]", "\r\n")
        s.send(req.encode())
        response = s.recv(4096).decode('utf-8', errors='ignore')
        s.close()
        status = response.split()[1] if "HTTP/1.1" in response else "NO-HTTP"
        cdn = "CloudFront" if "X-Amz-Cf-Id" in response else "Cloudflare" if "CF-RAY" in response else "Direct"

        if status in allowed_codes:
            with lock:
                sent += 1; live_count += 1
                stats[status] = stats.get(status, 0) + 1
                results_buffer.append(f"{target} | {ip} | {status} | {cdn}\n")
                print(f"{Fore.GREEN}[LIVE] {target} -> {ip} - HTTP {status}{Style.RESET_ALL}")
        elif status == "302":
            with lock:
                sent += 1; redirect_count += 1
                print(f"{Fore.RED}[302] {target} -> {ip} - REDIRECT{Style.RESET_ALL}")
        else:
            with lock:
                sent += 1
                stats["OTHER"] += 1
    except:
        with lock: sent += 1

def print_status(start_time, total, threads):
    while sent < total:
        time.sleep(0.3)
        elapsed = time.time() - start_time
        speed = sent / elapsed if elapsed > 0 else 0
        sys.stdout.write(f"\033[1A\033[2K{Fore.YELLOW}Threads:{threads} Checked:{sent}/{total} LIVE:{live_count} 302:{redirect_count} Speed:{speed:.0f}/s{Style.RESET_ALL}\n")
        sys.stdout.flush()

def main():
    print(BANNER)
    print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} Scan CIDR")
    print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Scan Domain File")
    mode = input(f"{Fore.YELLOW}Select: {Style.RESET_ALL}")

    target_list = []; is_domain = False
    if mode == "1":
        cidr = input(f"{Fore.YELLOW}CIDR: {Style.RESET_ALL}")
        target_list = generate_ips_from_cidr(cidr)
    elif mode == "2":
        file_path = input(f"{Fore.YELLOW}File Path [/sdcard/Download/domains.txt]: {Style.RESET_ALL}") or "/sdcard/Download/domains.txt"
        if not os.path.exists(file_path): print(f"{Fore.RED}[!] File nahi mili{Style.RESET_ALL}"); sys.exit()
        with open(file_path) as f: target_list = [line.strip() for line in f if line.strip()]
        is_domain = True; print(f"{Fore.GREEN}[+] {len(target_list)} Domains loaded{Style.RESET_ALL}")
    else: print(f"{Fore.RED}[!] Invalid{Style.RESET_ALL}"); sys.exit()

    user_payload = input(f"{Fore.YELLOW}Payload [Enter for Default]: {Style.RESET_ALL}")
    payload = user_payload if user_payload.strip()!= "" else DEFAULT_PAYLOAD
    port = int(input(f"{Fore.YELLOW}Port [80]: {Style.RESET_ALL}") or 80)
    threads = int(input(f"{Fore.YELLOW}Threads [500]: {Style.RESET_ALL}") or 500)
    total = len(target_list)

    print(f"\n{Fore.GREEN}[+] Total: {total} | Threads: {threads}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}[LOG REGISTER]{Style.RESET_ALL}\n" + "-"*80)

    output_file = f"KoSh_LIVE_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_path = f"/sdcard/Download/{output_file}"
    start_time = time.time()
    threading.Thread(target=print_status, args=(start_time, total, threads), daemon=True).start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(lambda t: scan_target(t, payload, port, is_domain), target_list)

    with open(save_path, "w") as f:
        f.write("TARGET | IP | STATUS | CDN\n"); f.writelines(results_buffer)

    print(f"\n{Fore.CYAN}✅ Done! File: {save_path}{Style.RESET_ALL}")
    summary = " | ".join([f"{k}:{v}" for k,v in stats.items() if v>0])
    print(f"{Fore.CYAN}TOTAL LIVE: {live_count} | 302 REDIRECT: {redirect_count} | {summary}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
