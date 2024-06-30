import pytest
import requests
import base64

# Это базовый URL для API
BASE_URL = "https://demo.3divi.ai/face-detector-face-fitter/v2/process/sample"

# Функция для кодирования изображения в base64
def encode_image_to_base64(image_path):
    # Открываем файл изображения
    image_file = open(image_path, "rb")
    # Читаем содержимое файла
    image_data = image_file.read()
    # Кодируем содержимое в base64
    encoded_data = base64.b64encode(image_data)
    # Декодируем в строку
    encoded_string = encoded_data.decode('utf-8')
    # Закрываем файл
    image_file.close()
    return encoded_string

# Тест для проверки успешной детекции лица
def test_successful_face_detection():
    # Путь к изображению
    image_path = './rayan.jpeg'
    # Кодируем изображение
    encoded_image = encode_image_to_base64(image_path)
    # Создаем тело запроса
    payload = {
        "_image": {
            "blob": encoded_image
        }
    }
    # Отправляем запрос
    response = requests.post(BASE_URL, json=payload)
    # Проверяем статус код
    assert response.status_code == 200
    # Преобразуем ответ в JSON
    data = response.json()
    # Проверяем наличие ключа 'objects'
    assert 'objects' in data
    # Проверяем, что есть хотя бы один объект
    assert len(data['objects']) > 0
    # Проверяем, что первый объект - это лицо
    assert data['objects'][0]['class'] == 'face'

# Тест для проверки невалидного формата изображения
def test_invalid_image_format():
    # Путь к невалидному изображению
    image_path = './rayan_invalid.xlsx'
    # Кодируем изображение
    encoded_image = encode_image_to_base64(image_path)
    # Создаем тело запроса
    payload = {
        "_image": {
            "blob": encoded_image
        }
    }
    # Отправляем запрос
    response = requests.post(BASE_URL, json=payload)
    # Проверяем статус код
    assert response.status_code == 422
    # Преобразуем ответ в JSON
    data = response.json()
    # Проверяем наличие ключа 'detail'
    assert 'detail' in data
    # Проверяем, что есть сообщение об ошибке для ключа 'blob'
    assert any(item['loc'] == ['body', '_image', 'blob'] for item in data['detail'])

# Тест для проверки случая, когда изображение не предоставлено
def test_no_image_provided():
    # Создаем пустое тело запроса
    payload = {}
    # Отправляем запрос
    response = requests.post(BASE_URL, json=payload)
    # Проверяем статус код
    assert response.status_code == 422
    # Преобразуем ответ в JSON
    data = response.json()
    # Проверяем наличие ключа 'detail'
    assert 'detail' in data
    # Проверяем, что есть сообщение об ошибке для ключа '_image'
    assert any(item['loc'] == ['body', '_image'] for item in data['detail'])

# Тест для проверки детекции нескольких лиц
def test_multiple_faces_detection():
    # Путь к изображению с несколькими лицами
    image_path = 'multiple_faces.jpg'
    # Кодируем изображение
    encoded_image = encode_image_to_base64(image_path)
    # Создаем тело запроса
    payload = {
        "_image": {
            "blob": encoded_image
        }
    }
    # Отправляем запрос
    response = requests.post(BASE_URL, json=payload)
    # Проверяем статус код
    assert response.status_code == 200
    # Преобразуем ответ в JSON
    data = response.json()
    # Проверяем наличие ключа 'objects'
    assert 'objects' in data
    # Проверяем, что есть более одного объекта
    assert len(data['objects']) > 1
    # Проверяем, что все объекты - это лица
    for obj in data['objects']:
        assert obj['class'] == 'face'

# Запускаем все тесты
if __name__ == "__main__":
    pytest.main()