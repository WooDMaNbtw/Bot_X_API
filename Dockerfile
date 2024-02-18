# Используем базовый образ Python 3.11
FROM python:3.11

# Добавляем /scripts в переменную PATH
ENV PATH="/scripts:${PATH}"

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Установка необходимых пакетов
RUN apt-get update && \
    apt-get install -y gcc libc-dev build-essential libpq-dev

# Установка зависимостей Python
RUN pip install -r requirements.txt

# Удаление ненужных пакетов
RUN apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создаем директорию /botX в контейнере
RUN mkdir /botX

# Создаем директорию /scripts в контейнере
RUN mkdir /scripts

# Копируем файлы из директории bot_x в /botX в контейнере
COPY bot_x /botX

# Устанавливаем рабочую директорию /botX
WORKDIR /botX

# Копируем скрипты из локальной директории scripts в /scripts в контейнере
COPY scripts /scripts

# Добавляем права на выполнение для всех скриптов в /scripts
RUN chmod +x /scripts/*

# Копируем entrypoint.sh в /scripts в контейнере
COPY scripts/entrypoint.sh /scripts/entrypoint.sh

# Добавляем права на выполнение для entrypoint.sh
RUN chmod +x /scripts/entrypoint.sh

# Запускаем entrypoint.sh при запуске контейнера
CMD ["entrypoint.sh"]
