# Импортируем необходимые библиотеки
import pytest  # Библиотека для написания и запуска тестов
import requests  # Библиотека для отправки HTTP-запросов
import base64  # Библиотека для кодирования и декодирования base64

# Определяем базовый URL для API
BASE_URL = "https://demo.3divi.ai/face-detector-face-fitter/v2/process/sample"

# Функция для кодирования изображения в формат base64
def encode_image_to_base64(image_path):
    # Открываем файл изображения в бинарном режиме
    with open(image_path, "rb") as image_file:
        # Кодируем содержимое файла в base64 и декодируем в строку
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# Тест для проверки успешной детекции лица
def test_successful_face_detection():
    # Путь к изображению для теста
    image_path = './rayan.jpeg'
    # Кодируем изображение в base64
    encoded_image = encode_image_to_base64(image_path)
    # Создаем payload (тело запроса) с закодированным изображением
    payload = {
        "_image": {
            "blob": encoded_image
        }
    }
    # Отправляем POST-запрос с payload на BASE_URL
    response = requests.post(BASE_URL, json=payload)

    # Проверяем, что статус код ответа 200 (успешный запрос)
    assert response.status_code == 200
    # Преобразуем ответ в JSON
    data = response.json()
    # Проверяем, что в ответе есть ключ 'objects'
    assert 'objects' in data
    # Проверяем, что в ответе есть хотя бы один объект
    assert len(data['objects']) > 0
    # Проверяем, что первый объект в ответе имеет класс 'face'
    assert data['objects'][0]['class'] == 'face'

# Тест для проверки обработки невалидного формата изображения
def test_invalid_image_format():
    # Путь к невалидному изображению для теста
    image_path = './rayan_invalid.xlsx'
    # Кодируем изображение в base64
    encoded_image = encode_image_to_base64(image_path)
    # Создаем payload с закодированным изображением
    payload = {
        "_image": {
            "blob": encoded_image
        }
    }
    # Отправляем POST-запрос с payload на BASE_URL
    response = requests.post(BASE_URL, json=payload)

    # Проверяем, что статус код ответа 422 (необрабатываемый объект)
    assert response.status_code == 422
    # Преобразуем ответ в JSON
    data = response.json()
    # Проверяем, что в ответе есть ключ 'detail'
    assert 'detail' in data
    # Проверяем, что в ответе есть сообщение об ошибке для ключа 'blob'
    assert any(item['loc'] == ['body', '_image', 'blob'] for item in data['detail'])

# Тест для проверки обработки случая, когда изображение не предоставлено
def test_no_image_provided():
    # Создаем пустой payload
    payload = {}
    # Отправляем POST-запрос с пустым payload на BASE_URL
    response = requests.post(BASE_URL, json=payload)

    # Проверяем, что статус код ответа 422 (необрабатываемый объект)
    assert response.status_code == 422
    # Преобразуем ответ в JSON
    data = response.json()
    # Проверяем, что в ответе есть ключ 'detail'
    assert 'detail' in data
    # Проверяем, что в ответе есть сообщение об ошибке для ключа '_image'
    assert any(item['loc'] == ['body', '_image'] for item in data['detail'])

# Тест для проверки детекции нескольких лиц на изображении
def test_multiple_faces_detection():
    # Путь к изображению с несколькими лицами для теста
    image_path = 'multiple_faces.jpg'
    # Кодируем изображение в base64
    encoded_image = encode_image_to_base64(image_path)
    # Создаем payload с закодированным изображением
    payload = {
        "_image": {
            "blob": encoded_image
        }
    }
    # Отправляем POST-запрос с payload на BASE_URL
    response = requests.post(BASE_URL, json=payload)

    # Проверяем, что статус код ответа 200 (успешный запрос)
    assert response.status_code == 200
    # Преобразуем ответ в JSON
    data = response.json()
    # Проверяем, что в ответе есть ключ 'objects'
    assert 'objects' in data
    # Проверяем, что в ответе есть более одного объекта
    assert len(data['objects']) > 1
    # Проверяем, что все объекты в ответе имеют класс 'face'
    for obj in data['objects']:
        assert obj['class'] == 'face'

# Запускаем все тесты, если скрипт запущен как основная программа
if __name__ == "__main__":
    pytest.main()