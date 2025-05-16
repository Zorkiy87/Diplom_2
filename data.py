

class Urls:
    base_url = 'https://stellarburgers.nomoreparties.site'
    url_create_user = f'{base_url}/api/auth/register'
    url_user_login = f'{base_url}/api/auth/login'
    url_delete_user = f'{base_url}/api/auth/user'
    url_update_user = f'{base_url}/api/auth/user'
    url_create_order = f'{base_url}/api/orders'
    url_get_order = f'{base_url}/api/orders'



class Ingredients:
    ingredients = ['61c0c5a71d1f82001bdaaa6d', '61c0c5a71d1f82001bdaaa73','61c0c5a71d1f82001bdaaa6f','61c0c5a71d1f82001bdaaa77']
    INCORRECT_INGREDIENT_HASH = '61c0c5a71d1f82025abcda6d'