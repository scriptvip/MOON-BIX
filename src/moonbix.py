import requests

from fake_useragent import UserAgent

from src.__init__ import *
class MoonBix:
    def __init__(self, token, proxy, timeout):
        self.session = requests.session()
        self.session.headers.update({
            'authority': 'www.binance.com',
            'accept': '*/*',
            'accept-language': 'en-EG,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'bnc-location': '',
            'clienttype': 'web',
            'content-type': 'application/json',
            'lang': 'en',
            'origin': 'https://www.binance.com',
            'referer': 'https://www.binance.com/en/game/tg/moon-bix',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': UserAgent().random
        })
        if proxy:
            self.session.proxies.update(proxy)

        self.timeout = timeout

        self.token = token if not is_url_encoded(token) else url_decode(token)
        
        self.game_response = None

    def login(self):
        json_data = {
            'queryString': self.token,
            'socialType': 'telegram',
        }
        
        response = self.session.post(
            'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/third-party/access/accessToken',
            json=json_data,
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            return 'fail'

        data = response.json()
        
        accessToken = data['data']['accessToken']

        self.session.headers['x-growth-token']= accessToken
        
        

        return 'success'
    
    def daily_login(self):
        json_data = {
            'resourceIdList': [
                2057,
            ],
            'referralCode': None,
        }
        response = self.session.post(
            'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/task/complete',
            json=json_data,
        )
        res = response.json()
        if 'data' in res:
            if res['data'] and res['data'].get('type', None)=='LOGIN':
                return 'claimed'
            return 'already_claimed'
        return response.text
    

    def user_info(self):
        json_data = {
            'resourceId': 2056,
        }
        response = self.session.post(
            'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/user/user-info',
            json=json_data,
            timeout=self.timeout
        )
        
        return response.json()
    
    def start_game(self):
        json_data = {
            'resourceId': 2056,
        }
        
        response = self.session.post(
            'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/start',
            json=json_data,
            timeout=self.timeout
        )


        self.game_response = response.json()
        
        if response.json()['code'] == '000000':
            return 'success'
        
        if response.json()['code'] == '116002':
            return 'attempts not enough'
        else:
            return response.text
    
    def game_data(self, key):
        url = config('API', 'NOT SET')+'/moonbix/api/v1/play'

        data = {
            'key': key,
            'game_response': self.game_response
        }
        if url == 'NOT SET':
            log(f'{Colors.RED} Please Set the API !')
            return 'fail', 1

        response = requests.get(url, json=data, timeout=self.timeout)
        res = response.json()
        if res['message']=='success':
            self.game = res['game']
            return 'success', response.status_code
        
        return 'fail', response.status_code
        

    def complete_game(self):
        
        json_data = {
            'resourceId': 2056,
            'payload': self.game['payload'],
            'log': self.game['log'],
        }

        response = self.session.post(
            'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/complete',
            json=json_data,
            timeout=self.timeout
        )

        if  response.json()['success']:
            return 'success'
        
        return response.text

