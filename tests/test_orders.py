import allure  # Импортируем Allure для оформления тестов
from helpers.data import EMPTY_INGREDIENTS, INVALID_INGREDIENTS  # Тестовые данные для заказов
from helpers.messages import INGREDIENTS_REQUIRED_MESSAGE  # Сообщение об ошибке при отсутствии ингредиентов
from helpers.urls import ORDERS_URL, INGREDIENTS_URL  # Ручки для создания заказа и получения ингредиентов

@allure.title("Создание заказа с авторизацией")  # Заголовок отчёта Allure
def test_create_order_authorized(registered_user, session):  # Тест на создание заказа авторизованным пользователем
    ingredients_response = session.get(INGREDIENTS_URL)  # Получаем список доступных ингредиентов
    ingredients = ingredients_response.json()["data"]  # Получаем данные ингредиентов
    ingredient_id = ingredients[0]["_id"]  # Берём идентификатор первого ингредиента

    order_data = {"ingredients": [ingredient_id]}  # Подготавливаем данные заказа
    headers = {"Authorization": registered_user["access_token"]}  # Добавляем токен авторизации

    response = session.post(ORDERS_URL, json=order_data, headers=headers)  # Отправляем запрос на создание заказа

    assert response.status_code == 200  # Проверяем успешный статус ответа
    assert response.json()["success"] is True  # Проверяем успешное создание заказа
    assert "number" in response.json()["order"]  # Проверяем наличие номера заказа

@allure.title("Создание заказа без авторизации")  # Заголовок отчёта Allure
def test_create_order_unauthorized(session):  # Тест на создание заказа неавторизованным пользователем
    ingredients_response = session.get(INGREDIENTS_URL)  # Получаем список доступных ингредиентов
    ingredients = ingredients_response.json()["data"]  # Получаем данные ингредиентов
    ingredient_id = ingredients[0]["_id"]  # Берём идентификатор первого ингредиента

    order_data = {"ingredients": [ingredient_id]}  # Подготавливаем данные заказа

    response = session.post(ORDERS_URL, json=order_data)  # Отправляем запрос без токена авторизации

    assert response.status_code == 200  # Проверяем успешный статус ответа
    assert response.json()["success"] is True  # Проверяем успешное создание заказа
    assert "number" in response.json()["order"]  # Проверяем наличие номера заказа

@allure.title("Создание заказа без ингредиентов")  # Заголовок отчёта Allure
def test_create_order_without_ingredients(session):  # Тест на создание заказа без ингредиентов
    order_data = {"ingredients": EMPTY_INGREDIENTS}  # Подготавливаем заказ с пустым списком ингредиентов

    response = session.post(ORDERS_URL, json=order_data)  # Отправляем запрос на создание заказа

    assert response.status_code == 400  # Проверяем статус ошибки
    assert response.json()["message"] == INGREDIENTS_REQUIRED_MESSAGE  # Проверяем текст ошибки

@allure.title("Создание заказа с неправильным идентификатором ингредиента")  # Заголовок отчёта Allure
def test_create_order_with_incorrect_ingredient(session):  # Тест на создание заказа с неправильным ингредиентом
    order_data = {"ingredients": INVALID_INGREDIENTS}  # Подготавливаем заказ с неправильным идентификатором ингредиента

    response = session.post(ORDERS_URL, json=order_data)  # Отправляем запрос на создание заказа

    assert response.status_code == 500  # Проверяем статус ошибки сервера согласно документации