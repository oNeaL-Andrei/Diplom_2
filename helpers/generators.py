from faker import Faker  # Импортируем библиотеку Faker для генерации случайных данных

fake = Faker()  # создаём экземпляр Faker для генерации случайных данных

def generate_user_data():  # Функция для гененрации случайных данных пользователем
    return {"email": fake.email(),"password": fake.password(),"name": fake.name()}