import allure  # Импортируем Allure для оформления тестов
from helpers.messages import USER_ALREADY_EXISTS, REQUIRED_FIELDS_MESSAGE  # Сообщения об ошибках
from helpers.urls import REGISTER_URL  # Ручка для регистрации пользователя
from helpers.generators import generate_user_data  # Генератор данных пользователя

@allure.title("Успешная регистрация уникального пользователя")  # Заголовок отчёта Allure
def test_user_registration_success(registered_user):  # Тест на успешную регистрацию уникального пользователя
    response = registered_user["response"]  # Получаем ответ на регистрацию из фикстуры

    assert response.status_code == 200  # Проверяем успешный статус ответа
    assert response.json()["success"] is True  # Проверяем успешную регистрацию
    assert "accessToken" in response.json()  # Проверяем наличие токена авторизации
    assert "refreshToken" in response.json()  # Проверяем наличие токена обновления

@allure.title("Повторная регистрация пользователя")  # Заголовок отчёта Allure
def test_user_registration_duplicate(registered_user, session):  # Тест на повторную регистрацию уже существующего пользователя
    response = session.post(REGISTER_URL, json=registered_user["data"])  # Отправляем данные уже зарегистрированного пользователя

    assert response.status_code == 403  # Проверяем статус ошибки повторной регистрации
    assert response.json()["message"] == USER_ALREADY_EXISTS  # Проверяем текст ошибки

@allure.title("Регистрация без обязательного поля")  # Заголовок отчёта Allure
def test_user_registration_without_required_field(session):  # Тест на регистрацию без обязательного поля (имени пользователя)
    user_data = generate_user_data()  # Создаём данные нового пользователя
    user_data.pop("name")  # Удаляем имя, чтобы проверить регистрацию без обязательного поля

    response = session.post(REGISTER_URL, json=user_data)  # Отправляем запрос без имени

    assert response.status_code == 403  # Проверяем статус ошибки
    assert response.json()["message"] == REQUIRED_FIELDS_MESSAGE  # Проверяем текст ошибки