import requests
import allure

from data import Urls, Ingredients
from helpers import get_access_token


@allure.description('Тестирование класса получения заказов')
class TestGetOrders:
    @allure.title('Проверяем получение заказов без авторизации пользователя')
    def test_get_order_to_not_auth_user(self):
        with allure.step('Подготавливаем заголовок'):
            headers = {
                'Content-Type': 'application/json'
            }
        with allure.step('Делаем запрос с подготовленными данными'):
            response = requests.get(Urls.url_get_order, headers=headers)
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
            assert response.json()['message'] == "You should be authorised"
            assert response.json()['success'] == False

    @allure.title('Проверяем получение заказов с авторизацией пользователя')
    def test_get_order_to_auth_user(self, registration_and_delete_user):
        with allure.step('Создаём зарегистрированного пользователя'):
            payload, response = registration_and_delete_user
        with allure.step('Подготавливаем данные для запроса (ингредиенты)'):
            new_payload = {'ingredients': Ingredients.ingredients}
        with allure.step('Получаем ключ доступа для запроса'):
            access_token = get_access_token(response)
        with allure.step('Подготавливаем заголовок'):
            headers = {
                'Authorization': f'{access_token}',
            }
        with allure.step('Создаём заказ с подготовленными данными'):
            requests.post(Urls.url_create_order, json=new_payload, headers=headers)
        with allure.step('Получаем сделанный пользователем заказ'):
            new_response = requests.get(Urls.url_get_order, headers=headers)
        order = new_response.json()
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert new_response.status_code == 200, f"Ожидался статус 200, но получен {new_response.status_code}"
            assert 'orders' in order.keys()
            assert 'total' in order.keys()