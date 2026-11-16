import pytest  # Импортируем библиотеку для запуска тестов
import requests  # Импортируем библиотеку для HTTP-запросов
import allure  # Импортируем Allure для оформления шагов

from helpers.generators import generate_user_data  # Импортируем функцию для генерации случайныхх данных пользователя
from helpers.urls import REGISTER_URL, USER_URL  # Импортируем ручки для регистрации и удаления пользователя

@pytest.fixture  # Создаём HTTP-сессию для теста и закрываем её после завершения
def session():
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture  # Создаём тестового пользователя и удаляем его после завершения теста
def registered_user(session):
    user_data = generate_user_data()
    with allure.step("Создаём тестового пользователя"):
        response = session.post(REGISTER_URL, json=user_data)
    access_token = response.json()["accessToken"]
    yield {"data": user_data, "response": response, "access_token": access_token}
    with allure.step("Удаляем тестового пользователя"):
        session.delete(USER_URL, headers={"Authorization": access_token})