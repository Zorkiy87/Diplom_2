import requests
import allure

from data import Urls, Ingredients
from helpers import get_access_token


@allure.description('Тестирование класса получения заказов')
class TestGetOrders:
    @allure.title('Проверяем получение заказов без авторизации пользователя')
    def test_get_order_to_not_auth_user(self):
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.get(Urls.url_get_order, headers=headers)

        assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
        assert response.json()['message'] == "You should be authorised"
        assert response.json()['success'] == False

    @allure.title('Проверяем получение заказов с авторизацией пользователя')
    def test_get_order_to_auth_user(self, registration_and_delete_user):
        payload, response = registration_and_delete_user
        new_payload = {'ingredients': Ingredients.ingredients}
        access_token = get_access_token(response)
        headers = {
            'Authorization': f'{access_token}',
        }
        requests.post(Urls.url_create_order, json=new_payload, headers=headers)
        new_response = requests.get(Urls.url_get_order, headers=headers)
        order = new_response.json()
        assert new_response.status_code == 200, f"Ожидался статус 200, но получен {new_response.status_code}"
        assert 'orders' in order.keys()
        assert 'total' in order.keys()
