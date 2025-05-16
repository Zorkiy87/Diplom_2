import allure
import requests

from helpers import generate_random_email_password_name
from data import Urls


@allure.description('Тестирование класса обновления данных пользователя')
class TestUpdateUserData:
    @allure.title('Проверяем возможность обновления данных у авторизованного пользователя')
    @allure.description('Проверяем, что любое поле можно изменить, проверка кода ответа')
    def test_update_user_data_to_auth_user(self, registration_and_delete_user):
        payload, response = registration_and_delete_user
        new_payload = generate_random_email_password_name()
        access_token = response.json().get('accessToken')
        headers = {
            'Authorization': f'{access_token}',
            'Content-Type': 'application/json'
        }
        new_response = requests.patch(Urls.url_update_user,headers=headers,json=new_payload)
        assert new_response.status_code == 200, f"Ожидался статус 200, но получен {new_response.status_code}"
        assert new_response.json()['user']['email'] == new_payload['email']
        assert new_response.json()['user']['name'] == new_payload['name']

    @allure.title('Проверяем невозможность обновления данных у неавторизованного пользователя')
    @allure.description('Проверяем, что возвращается ошибка при изменении данных у неавторизованного пользователя')
    def test_update_user_data_to_not_auth_user_error(self):
        new_payload = generate_random_email_password_name()
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.patch(Urls.url_update_user,headers=headers,json=new_payload)
        assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
        assert response.json()['message'] == "You should be authorised", \
            f"Ожидалось сообщение 'You should be authorised, но получен ответ {response.json()['message']}"
        assert response.json()['success'] == False, \
            f"Ожидался ответ False, но получен ответ {response.json()['success']}"