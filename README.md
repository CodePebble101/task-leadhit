# Тестовое задание для компании LeadHit
## Web-приложение для определения заполненных форм
***


### Сборка и запуск
После клонирования репозитория необходимо открыть консоль в корневой папке проекта и ввести команду:
- docker-compose build && docker-compose up -d
____________________
После окончания сборки проекта интерактивная документация появится на адресе
- http://localhost:10090
____________________
### Тесты
По дефолту тесты запускаются сразу после старта проекта внутри отдельного контейнера (сервис tests). Посмотреть
результаты прошедших тестов:
- docker container logs -f TL_Tests
#### Перезапустить тесты:
- docker-compose restart tests

____________________
### Стек
- FastAPI
- MongoDB
- Redis
- Docker
____________________
### Структура папок
├───app - основная папка проекта  
│   ├───auth - сервис авторизации  
│   ├───config - основные настройки приложения  
│   ├───endpoints - все самописные эндпоинты  
│   ├───models  
│   │   ├───validation - модели данных для валидации эндпоинтов  
│   ├───scripts - скрипты для слоя бизнес-логики  
├───tests - папка с тестами API  
____________________
