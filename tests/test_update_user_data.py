import allure
import requests

from helpers import generate_random_email_password_name
from data import Urls


@allure.description('Тестирование класса обновления данных пользователя')
class TestUpdateUserData:
    @allure.title('Проверяем возможность обновления данных у авторизованного пользователя')
    @allure.description('Проверяем, что любое поле можно изменить, проверка кода ответа')
    def test_update_user_data_to_auth_user(self, registration_and_delete_user):
        with allure.step('Создаём зарегистрированного пользователя'):
            payload, response = registration_and_delete_user
        with allure.step('Генерируем новые данные для запроса'):
            new_payload = generate_random_email_password_name()
        with allure.step('Получаем ключ доступа для запроса'):
            access_token = response.json().get('accessToken')
        with allure.step('Подготавливаем заголовок'):
            headers = {
                'Authorization': f'{access_token}',
                'Content-Type': 'application/json'
            }
        with allure.step('Делаем запрос на обновление с подготовленными данными'):
            new_response = requests.patch(Urls.url_update_user,headers=headers,json=new_payload)
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert new_response.status_code == 200, f"Ожидался статус 200, но получен {new_response.status_code}"
            assert new_response.json()['user']['email'] == new_payload['email']
            assert new_response.json()['user']['name'] == new_payload['name']

    @allure.title('Проверяем невозможность обновления данных у неавторизованного пользователя')
    @allure.description('Проверяем, что возвращается ошибка при изменении данных у неавторизованного пользователя')
    def test_update_user_data_to_not_auth_user_error(self):
        with allure.step('Создаём зарегистрированного пользователя'):
            new_payload = generate_random_email_password_name()
        with allure.step('Подготавливаем заголовок'):
            headers = {
                'Content-Type': 'application/json'
            }
        with allure.step('Делаем запрос на обновление с подготовленными данными'):
            response = requests.patch(Urls.url_update_user,headers=headers,json=new_payload)
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
            assert response.json()['message'] == "You should be authorised", \
                f"Ожидалось сообщение 'You should be authorised, но получен ответ {response.json()['message']}"
            assert response.json()['success'] == False, \
                f"Ожидался ответ False, но получен ответ {response.json()['success']}"