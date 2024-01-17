import argparse
import requests
import string
import time
import random
import urllib.parse
import concurrent.futures
import signal
import sys

credit = '''
 ___________
< Want to find secret directories? >
 -----------                           /\      /
        \   ^__^  #github             /  \/\  /
         \  (oo)\_______           /\/      \/
            (__)\       )\/\      /   social
                ||----w |   \  /\/  credit pov
                ||     ||    \/
==============="Made By Bjorki199"================
'''

class DirectoryScanner:
    def __init__(self, url, wordlist_path, timeout, save_file, verbose, random_user_agent, calendar, threads, proxy):
        self.url = url
        self.timeout = timeout
        self.wordlist_path = wordlist_path
        self.save_file = save_file
        self.verbose = verbose
        self.random_user_agent = random_user_agent
        self.calendar = calendar
        self.threads = min(max(threads, 1), 20)
        self.proxy = proxy
        self.found_directories = 0

    def generate_random_calendar(self):
        days = list(map(str, range(1, 32)))
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        years = list(map(str, range(2000, 2023)))

        random_date = f"{random.choice(days)} {random.choice(months)} {random.choice(years)}"
        return random_date

    def get_random_user_agent(self):
        user_agents = {
            'android': [
                'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 9; SM-G950U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
            ],
            'desktop': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
            ]
        }
        proxy = self.get_random_proxy() if self.proxy == 'random' else self.proxy
        return random.choice(random.choice(list(user_agents.values())))

    def get_random_proxy(self):
        from fp.fp import FreeProxy
        return FreeProxy(elite=True).get()

    def find_directory(self, directory):
        full_url = f"{self.url}/{directory}"
        headers = {'User-Agent': self.get_random_user_agent() if self.random_user_agent else ''}
        proxies = None

        if self.proxy and self.proxy != 'random':
            proxies = {"http": self.proxy, "https": self.proxy}
            
        try:
            response = requests.get(full_url, headers=headers, proxies=proxies, timeout=self.timeout)
            response.raise_for_status()
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                if self.verbose:
                    print(f"\033[91m[-] 404 Not Found: {full_url}\033[0m")
            else:
                if self.verbose:
                    print(f"\033[91m[-] Failed to access: {full_url} ({e})\033[0m")
        except requests.RequestException as e:
            if self.verbose:
                print(f"\033[91m[-] Failed to access: {full_url} ({e})\033[0m")
        else:
            self.found_directories += 1
            if self.verbose:
                print(f"\033[92m[+] Directory found: {full_url}\033[0m")
            with open(self.save_file, 'a') as save_file:
                save_file.write(f"{full_url}\n")

    def find_directories(self):
        with open(self.wordlist_path, 'r') as file:
            directories = [line.strip() for line in file.readlines()]

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.find_directory, directory) for directory in directories]

    def signal_handler(self, sig, frame):
        print("\n\nScanning Statistics:")
        print(f"Directories found: {self.found_directories}")
        sys.exit(0)

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        if self.calendar == 'random':
            random_date = self.generate_random_calendar()
            print(f"Using random date: {random_date}")
            time_tuple = time.strptime(random_date, "%d %B %Y")
            timestamp = int(time.mktime(time_tuple))
            self.url = f"{self.url}/{timestamp}"

        print("\nScanning...\n")
        self.find_directories()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="argumen untuk mencari directory dari sebuah website menggunakan wordlist")
    parser.add_argument('-u', '--url', required=True, help='URL target website')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Waktu timeout untuk setiap request (detik)')
    parser.add_argument('-rua', '--random_user_agent', action='store_true', help='Gunakan user agent secara acak')
    parser.add_argument('-c', '--calendar', choices=['random', 'default'], default='default', help='Pilih calendar (random/default)')
    parser.add_argument('-l', '--wordlist', required=True, help='Path ke file wordlist')
    parser.add_argument('-s', '--save', help='Nama file untuk menyimpan hasil nama.txt')
    parser.add_argument('-v', '--verbose', action='store_true', help='Tampilkan output detail seperti 404 dll')
    parser.add_argument('-th', '--threads', type=int, default=1, choices=range(1, 21), help='Jumlah multi-thread (1-20) lebih besar lebih cepat')
    parser.add_argument('-p', '--proxy', default=None, help='Alamat IP dan port proxy (contoh: http://ipadress:port) atau "random" untuk proxy acak')

    args = parser.parse_args()

    if args.proxy == 'random':
        from fp.fp import FreeProxy
    print(credit)
    scanner = DirectoryScanner(args.url, args.wordlist, args.timeout, args.save, args.verbose, args.random_user_agent, args.calendar, args.threads, args.proxy)
    scanner.run()
