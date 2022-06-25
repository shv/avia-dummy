# Заглушка для фронта по задаче поиска авиабилетов
## Запуск локально

`python manage.py runserver`

## Запуск в докере

`docker build ./`
`docker run -p 8085:8085 -e DJANGO_SECRET_KEY=qqq 51dd592923e75151`

DJANGO_SECRET_KEY - не обязательно
