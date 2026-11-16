import allure  # Импортируем Allure для оформления тестов

from helpers.data import INVALID_EMAIL, INVALID_PASSWORD  # Тестовые данные для неправильной авторизации
from helpers.messages import INCORRECT_CREDENTIALS_MESSAGE  # Сообщение об ошибке авторизации
from helpers.urls import LOGIN_URL  # Ручка для авторизации пользователя

@allure.title("Успешная авторизация существующего пользователя")  # Заголовок отчёта Allure
def test_user_login_success(registered_user, session):  # Тест на успешную авторизацию существующего пользователя
    user_data = registered_user["data"]  # Получаем данные зарегистрированного пользователя
    login_data = {"email": user_data["email"], "password": user_data["password"]}  # Подготавливаем данные для авторизации

    response = session.post(LOGIN_URL, json=login_data)  # Отправляем запрос на авторизацию

    assert response.status_code == 200  # Проверяем успешный статус ответа
    assert response.json()["success"] is True  # Проверяем успешную авторизацию
    assert "accessToken" in response.json()  # Проверяем наличие токена авторизации
    assert "refreshToken" in response.json()  # Проверяем наличие токена обновления

@allure.title("Авторизация с неправильными учётными данными")  # Заголовок отчёта Allure
def test_user_login_incorrect_credentials(session):  # Тест на авторизацию с неправильными email и паролем
    login_data = {"email": INVALID_EMAIL, "password": INVALID_PASSWORD}  # Подготавливаем неправильные данные для авторизации

    response = session.post(LOGIN_URL, json=login_data)  # Отправляем запрос на авторизацию

    assert response.status_code == 401  # Проверяем статус ошибки авторизации
    assert response.json()["message"] == INCORRECT_CREDENTIALS_MESSAGE  # Проверяем текст ошибки