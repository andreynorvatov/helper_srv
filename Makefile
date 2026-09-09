# Переменные
IMAGE_NAME := helper
IMAGE_TAG := latest
IMAGE_FULL := $(IMAGE_NAME):$(IMAGE_TAG)
TAR_FILE := $(IMAGE_NAME).tar

# Данные сервера
SERVER_USER := admin
SERVER_HOST := amzng
SERVER_PATH := ~/test_srv

# Docker опции
DOCKER_PORT := 8000

.PHONY: help build save copy load run clean all

help:
	@echo "Доступные команды:"
	@echo "  make build    - Собрать Docker образ"
	@echo "  make save     - Сохранить образ в tar файл"
	@echo "  make copy     - Скопировать tar файл на сервер"
	@echo "  make load     - Загрузить образ на сервере"
# 	@echo "  make run      - Запустить контейнер на сервере"
	@echo "  make all      - Выполнить все шаги последовательно"
	@echo "  make clean    - Удалить tar файл локально"
	@echo "  make run    - Удалить tar файл локально"

build:
	docker build -t $(IMAGE_FULL) .

save: build
	docker save -o $(TAR_FILE) $(IMAGE_FULL)
	@echo "Образ сохранен в $(TAR_FILE)"

copy: save
	scp $(TAR_FILE) $(SERVER_USER)@$(SERVER_HOST):$(SERVER_PATH)
	@echo "Файл скопирован на сервер"

load: copy
	ssh $(SERVER_USER)@$(SERVER_HOST) "docker load -i $(SERVER_PATH)$(TAR_FILE)"
	@echo "Образ загружен на сервере"

# run: load
# 	ssh $(SERVER_USER)@$(SERVER_HOST) "docker run -d -p $(DOCKER_PORT):$(DOCKER_PORT) --name $(IMAGE_NAME) $(IMAGE_FULL)"
# 	@echo "Контейнер запущен на порту $(DOCKER_PORT)"
run:
 uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Выполнить все шаги
all: run
	@echo "✅ Все операции выполнены успешно!"

# Остановить и удалить контейнер на сервере
stop:
	ssh $(SERVER_USER)@$(SERVER_HOST) "docker stop $(IMAGE_NAME) || true && docker rm $(IMAGE_NAME) || true"
	@echo "Контейнер остановлен и удален"

# Удалить образ с сервера
remove-image: stop
	ssh $(SERVER_USER)@$(SERVER_HOST) "docker rmi $(IMAGE_FULL) || true"
	@echo "Образ удален с сервера"

# Очистка локальных файлов
clean:
	rm -f $(TAR_FILE)
	@echo "Локальные файлы очищены"

# Полная очистка (локально и на сервере)
clean-all: remove-image clean
	@echo "✅ Полная очистка выполнена"