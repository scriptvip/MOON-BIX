from src.__init__ import *
from src.core import *
import requests

if __name__ == '__main__':
    
    awak()
    menu()
    while True:
        try:
            awak()
        except KeyboardInterrupt:
            exit_code()
        except requests.exceptions.ConnectionError:
            log(f'{Colors.RED} Connection Error !')
            log(f'{Colors.YELLOW} Please Check Network Connection !')
            log(f'{Colors.YELLOW} If You Connected To Internet Try Open CloudFlare DNS 1.1.1.1 becase your country is bocked from moonbix.')
            countdown_timer(60)
        except Exception as e:
            log(f'{Colors.RED} {e}')

    # tokens = load_tokens()
    # x = MoonBix(tokens[0])
    # x.login()
    # print(x.user_info())