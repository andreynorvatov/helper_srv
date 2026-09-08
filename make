# 1. Сохранить образ в файл
docker save -o my-app.tar my-app:latest

# 2. Скопировать на сервер через scp
scp my-app.tar user@server:/path/to/

# 3. На сервере загрузить образ из файла
ssh user@server
docker load -i /path/to/my-app.tar

# 4. Запустить контейнер
docker run -d -p 8000:8000 my-app:latest