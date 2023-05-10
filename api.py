import os
from time import sleep
import requests


class Api:

    def __init__(self):
        self.__app_id = 51641281
        self.__secret_key = os.environ['SECRET_KEY']
        self.__version = 5.131
        self.__redirect_url = 'https://oauth.vk.com/blank.html'

    def __get_all_friends(self, parsed: dict, token: str) -> dict:
        url = 'https://api.vk.com/method/friends.get' + \
              f"?userId={parsed.get('id')}" \
              f"&order=hints" \
              f"&count={10000 if parsed.get('count') is None else parsed.get('count')}" \
              f"&name_case=nom" \
              f"&access_token={token}" \
              f"&fields=first_name" \
              f"&v={self.__version}"

        response = requests.get(url=url).json()

        if response.get('response') is None:
            while response.get('error') is not None:
                sleep(0.01)
                response = requests.get(url=url).json()

        return response.get('response')

    def __get_followers(self, user_id: int, token: str):
        url = 'https://api.vk.com/method/users.getFollowers' + \
              f"?user_id={user_id}" \
              f"&access_token={token}" \
              f"&v={self.__version}"

        response = requests.get(url=url).json()

        if response.get('response') is None:
            while response.get('error') is not None:
                sleep(0.01)
                response = requests.get(url=url).json()

        return response.get('response')

    def get_top_friends(self, parsed: dict):
        req_url = f'https://oauth.vk.com/authorize' \
                  f'?client_id={self.__app_id}' \
                  f'&display=page' \
                  f'&scope=friends' \
                  f'&response_type=token' \
                  f'&v={self.__version}' \
                  f'&state=123456'

        print(f'Эту ссылку нужно открыть в браузере: {req_url}')
        print('И ввести query-параметр "access-token", который будет в url адресе: ')
        token = input()

        if token is None or len(token) == 0:
            print('Мы не смогли получить токен. Попробуйте позже.')
            return None

        response = self.__get_all_friends(parsed, token)

        friends = response.get('items')

        info_friends = list()

        for person in friends:
            user_id = person.get('id')
            followers = self.__get_followers(user_id, token)
            followers_count = followers.get('count') if followers is not None else 0

            info_friends.append({
                'id': user_id,
                'first_name': person.get('first_name'),
                'last_name': person.get('last_name'),
                'followers_count': followers_count
            })

        info_friends.sort(key=lambda key: key.get('followers_count'), reverse=True)

        return info_friends
