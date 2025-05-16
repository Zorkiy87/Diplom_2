import random
import string

import requests

from data import Urls


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def generate_random_email_password_name():
    # создаём словарь, чтобы метод мог его вернуть
    email_pass = {}

    # генерируем email, пароль и имя пользователя
    email_pass['email'] = f'{generate_random_string(7)}@yandex.ru'
    email_pass['password'] = generate_random_string(7)
    email_pass['name'] = generate_random_string(7)

    return email_pass

def generate_data_and_create_user():
    payload = generate_random_email_password_name()
    response = requests.post(Urls.url_create_user, json=payload)
    return payload, response

def get_access_token(response):
    return response.json().get('accessToken')