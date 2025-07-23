import pytest
import requests

from data import Urls
from helpers import generate_data_and_create_user


@pytest.fixture
def registration_and_delete_user():
    payload, response = generate_data_and_create_user()
    yield payload, response
    access_token = response.json().get('accessToken')
    requests.delete(Urls.url_delete_user, headers={'Authorization': access_token})