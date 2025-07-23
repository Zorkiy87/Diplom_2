import allure
import requests

from data import Urls
from helpers import *


@allure.description('Тестирование класса создания пользователя')
class TestCreateUser:

    @allure.title('Создаем нового пользователя, через рандом с уникальными данными')
    def test_create_new_user(self):
        with allure.step("Подготавливаем уникальные данные для регистрации"):
            payload = generate_random_email_password_name()
        with allure.step('Делаем запрос на регистрацию с подготовленными данными'):
            response = requests.post(Urls.url_create_user, json=payload)
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
            assert response.json()['success'] == True
            assert response.json()['user']['email'] == payload['email']
            assert response.json()['user']['name'] == payload['name']
        with allure.step('Получаем ключ доступа для запроса'):
            access_token = response.json().get('accessToken')
        with allure.step('Отправляем запрос на удаление созданного пользователя'):
            requests.delete(Urls.url_delete_user, headers={'Authorization': access_token})

    @allure.title('Проверка невозможности создания уже существующего пользователя')
    def test_cant_create_two_identical_users(self):
        with allure.step("Подготавливаем уникальные данные для регистрации"):
            payload = generate_random_email_password_name()
        with allure.step('Делаем запрос на регистрацию с подготовленными данными'):
            response = requests.post(Urls.url_create_user, json=payload)
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
            assert response.json()['success'] == True
            assert response.json()['user']['email'] == payload['email']
            assert response.json()['user']['name'] == payload['name']

        with allure.step("Запрос на создание пользователя с данными ранее зарегистрированного пользователя"):
            response2 = requests.post(Urls.url_create_user, json=payload)
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert response2.status_code == 403, f"Ожидался статус 403, но получен {response.status_code}"
            assert response2.json()['message'] == "User already exists", \
                f"Ожидалось сообщение 'User already exists', но получен ответ {response.json()['message']}"
            assert response2.json()['success'] == False, \
                f"Ожидался ответ False, но получен ответ {response.json()['success']}"
        with allure.step('Получаем ключ доступа для запроса'):
            access_token = response.json().get('accessToken')
        with allure.step('Отправляем запрос на удаление созданного пользователя'):
            requests.delete(Urls.url_delete_user, headers={'Authorization': access_token})

    @allure.title('Проверка появления ошибки при регистрации без передачи поля Email')
    def test_registration_without_a_email_failed(self):
        with allure.step("Подготавливаем уникальные данные для регистрации"):
            payload = {
                'password': generate_random_string(7),
                'name': generate_random_string(7)
            }
        with allure.step('Делаем запрос на регистрацию с подготовленными данными, без поля email'):
            response = requests.post(Urls.url_create_user, data=payload)
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert response.status_code == 403, f"Ожидался статус 403, но получен {response.status_code}"
            assert response.json()['message'] == "Email, password and name are required fields", \
                f"Ожидалось сообщение'Email, password and name are required fields', но получен ответ {response.json()['message']}"
            assert response.json()['success'] == False, \
                f"Ожидался ответ False, но получен ответ {response.json()['success']}"

    @allure.title('Проверка появления ошибки при регистрации без передачи поля password ')
    def test_registration_without_a_password_failed(self):
        with allure.step("Подготавливаем уникальные данные для регистрации"):
            payload = {
                'email': f'{generate_random_string(7)}@yandex.ru',
                'name': generate_random_string(7)
            }
        with allure.step('Делаем запрос на регистрацию с подготовленными данными, без поля password'):
            response = requests.post(Urls.url_create_user, data=payload)
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert response.status_code == 403, f"Ожидался статус 403, но получен {response.status_code}"
            assert response.json()['message'] == "Email, password and name are required fields", \
                f"Ожидалось сообщение'Email, password and name are required fields', но получен ответ {response.json()['message']}"
            assert response.json()['success'] == False, \
                f"Ожидался ответ False, но получен ответ {response.json()['success']}"

    @allure.title('Проверка появления ошибки при регистрации без передачи поля name')
    def test_registration_without_a_name_failed(self):
        with allure.step("Подготавливаем уникальные данные для регистрации"):
            payload = {
                'email': f'{generate_random_string(7)}@yandex.ru',
                'password': generate_random_string(7)
            }
        with allure.step('Делаем запрос на регистрацию с подготовленными данными, без поля name'):
            response = requests.post(Urls.url_create_user, data=payload)
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert response.status_code == 403, f"Ожидался статус 403, но получен {response.status_code}"
            assert response.json()['message'] == "Email, password and name are required fields", \
                f"Ожидалось сообщение'Email, password and name are required fields', но получен ответ {response.json()['message']}"
            assert response.json()['success'] == False, \
                f"Ожидался ответ False, но получен ответ {response.json()['success']}"