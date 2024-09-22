# This file can be empty, it just indicates that this directory should be treated as a package
import os
import json
import time
from datetime import datetime
from colorama import *
import random
from urllib.parse import parse_qs

class Colors:
    RED = Fore.LIGHTRED_EX
    WHITE = Fore.LIGHTWHITE_EX
    GREEN = Fore.LIGHTGREEN_EX
    YELLOW = Fore.LIGHTYELLOW_EX
    BLUE = Fore.LIGHTBLUE_EX
    RESET = Style.RESET_ALL
    BLACK = Fore.LIGHTBLACK_EX
    CYAN = Fore.CYAN
    MAGENTA = Fore.LIGHTMAGENTA_EX

last_log_message = None

def _logo():
    cols = [Colors.BLACK, Colors.BLUE, Colors.CYAN, Colors.GREEN, Colors.RED, Colors.YELLOW, Fore.LIGHTMAGENTA_EX]
    banner = r"""
  ██████╗ ██╗     ██╗████████╗ ██████╗██╗  ██╗
 ██╔════╝ ██║     ██║╚══██╔══╝██╔════╝██║  ██║
 ██║  ███╗██║     ██║   ██║   ██║     ███████║
 ██║   ██║██║     ██║   ██║   ██║     ██╔══██║
 ╚██████╔╝███████╗██║   ██║   ╚██████╗██║  ██║
  ╚═════╝ ╚══════╝╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
"""
    i=len(banner)-1

    while i>-1:
        banner = f'{banner[:i]}{random.choice(cols)}{banner[i:]}'
        i -= random.randint(10, 15)
    return banner

def _banner():
    print(_logo())
    print(f"{Colors.BLUE} Devoloper Name : {Colors.GREEN}Abdo Sleem")
    print(f"{Colors.BLUE} Telegram Username : {Colors.YELLOW}@glitch_no")
    print(f"{Colors.BLUE} Telegram Channel : {Colors.YELLOW}https://t.me/automation_tools")

    

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_config():
    config_path = os.path.join(os.path.dirname(__file__), '../config.json')
    with open(config_path, 'r') as file:
        try:
            config_content = file.read()
            return json.loads(config_content)
        except json.JSONDecodeError as e:
            return {}
        
def log(message,*l, **kwargs):
    global last_log_message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flush = kwargs.pop('flush', False)
    end = kwargs.pop('end', '\n')
    if message != last_log_message:
        print(f"{Colors.BLACK}[{current_time}] {message}", flush=flush, end=end)
        last_log_message = message

def log_line():
    print(Colors.WHITE + "~" * 60)

def load_fake_file(filepath):
    with open(filepath, 'r') as file:
        fake_ips = json.load(file)
    return fake_ips

def awak():
    _clear()
    _banner()
    log_line()

def countdown_timer(seconds):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        print(f"{Colors.WHITE} Please wait until {h}:{m}:{s} ", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print(f"{Colors.WHITE} Please wait until {h}:{m}:{s} ", flush=True, end="\r")

def _number(number):
    return "{:,.0f}".format(number)

def get_username(token:str):
    return json.loads(parse_qs(token)['user'][0]).get('username', '<NOT SET>')

def config(name, default):
    with open("config.json", 'r') as file:
        config = json.load(file)
        return config.get(name, default)
    
def edit_config_value(name, value):
    with open("config.json", 'r') as file:
        config = json.loads(file.read())
    
    config[name] = value
    with open("config.json", 'w') as file:
        json.dump(config, file, indent=4)
    
    
def menu_item(i, name):
    print(f'   {Colors.BLUE}[{i}] {Colors.GREEN}{name}')


def load_tokens():
    with open('tokens.txt', 'r') as f:
        data = f.read().strip().split('\n')
    while '' in data:
        data.remove('')
    return data


def random_proxy():
    if not config('ENABLE_PROXY', 0): return None

    with open('proxies.txt') as f:
        proxy = random.choice(f.readlines())

    proxy = proxy.strip()
    if not proxy:
        return None
    proxy = {
        'http': proxy,
        'https': proxy
    }
    return proxy
