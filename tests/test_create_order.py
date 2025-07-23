import allure
import requests

from data import Ingredients, Urls
from helpers import get_access_token


@allure.description('Тестирование класса создания заказа')
class TestCreateOrder:
    @allure.title('Проверяем создание заказа с ингредиентами, когда пользователь авторизован')
    def test_create_order_to_auth_user(self, registration_and_delete_user):
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
        with allure.step('Делаем запрос с подготовленными данными'):
            new_response = requests.post(Urls.url_create_order, json=new_payload, headers=headers )

        order = new_response.json()
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert new_response.status_code == 200, f"Ожидался статус 200, но получен {new_response.status_code}"
            assert 'name' in order.keys()
            assert 'number' in order['order'].keys()

    @allure.title('Проверяем создание заказа с ингредиентами, когда пользователь не авторизован')
    def test_create_order_to_not_auth_user(self):
        with allure.step('Подготавливаем данные для запроса (ингредиенты)'):
            payload = {'ingredients': Ingredients.ingredients}
        with allure.step('Подготавливаем заголовок'):
            headers = {
                    'Content-Type': 'application/json'
                }
        with allure.step('Делаем запрос с подготовленными данными'):
            response = requests.post(Urls.url_create_order, json=payload, headers=headers )
        order = response.json()
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
            assert 'name' in order.keys()
            assert 'number' in order['order'].keys()

    @allure.title('Проверяем создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self):
        with allure.step('Подготавливаем данные для запроса (без ингредиентов)'):
            ingredients = {'ingredients': []}
        with allure.step('Делаем запрос с подготовленными данными'):
            response = requests.post(Urls.url_create_order, data=ingredients )
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"
            assert response.json()['message'] == "Ingredient ids must be provided"

    @allure.title('Проверяем создание заказа c несуществующим хэш ингредиента и авторизованным пользователем')
    def test_create_order_incorrect_ingredients_auth_user_error(self, registration_and_delete_user):
        with allure.step('Создаём зарегистрированного пользователя'):
            payload, response = registration_and_delete_user
        with allure.step('Подготавливаем данные для запроса (несуществующий ингредиент)'):
            new_payload = {'ingredients': Ingredients.INCORRECT_INGREDIENT_HASH}
        with allure.step('Получаем ключ доступа для запроса'):
            access_token = get_access_token(response)
        with allure.step('Подготавливаем заголовок'):
            headers = {
                'Authorization': f'{access_token}',
            }
        with allure.step('Делаем запрос с подготовленными данными'):
            new_response = requests.post(Urls.url_create_order, json=new_payload, headers=headers)
        with allure.step('Проверяем выполнение запроса, код ответа, содержание ответа'):
            assert new_response.status_code == 400, f"Ожидался статус 400, но получен {new_response.status_code}"
            assert new_response.json()['message'] == "One or more ids provided are incorrect"
            assert new_response.json()['success'] == False