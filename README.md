<<<<<<< HEAD
Для запуска приложения необходимо из корня проекта запустить команду "docker compose up". Перед этим в файле .env.docker нужно задать значения для OPENAI_KEY и URL_FOR_REQUEST задать соответствующие значения. Примеры отчетов к сожалению прикрепить не могу, тк ключа с возможностью запросов у меня не было. Краткоя описание архитектуры: Модульность. Логика разделена по папкам и модулям: обработка данных, тестирование, модели и задачи.

Поддержка асинхронности. Помимо celery все функции, запросы в БД и сама базы выполнены с использованием асинхронности.

Фоновая обработка. Celery используется для выполнения фоновых задач для отправки запроса на получение данных и их обработки.

Тестирование. Присутствуют тесты для проверки парсинга

Логирование. Настроена система логирования для мониторинга работы приложения. Логи будут доступны в корне проекта в файле my_logging.log
=======
Для запуска приложения необходимо из корня проекта запустить команду "docker compose up". Перед этим в файле .env.docker нужно задать значения для OPENAI_KEY и URL_FOR_REQUEST задать соответствующие значения.
Примеры отчетов к сожалению прикрепить не могу, тк ключа с возможностью запросов у меня не было. 
Краткоя описание архитектуры:
Модульность.
  Логика разделена по папкам и модулям: обработка данных, тестирование, модели и задачи.

Поддержка асинхронности.
  Помимо celery все функции, запросы в БД и сама базы выполнены с использованием асинхронности.

Фоновая обработка.
  Celery используется для выполнения фоновых задач для отправки запроса на получение данных и их обработки.

Тестирование.
  Присутствуют тесты для проверки парсинга

Логирование.
  Настроена система логирования для мониторинга работы приложения. Логи будут доступны в корне проекта в файле my_logging.log
>>>>>>> bd041448396b313103b2af7d52c32a8dca1f38ed
