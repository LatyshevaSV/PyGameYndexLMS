#!/bin/bash

# Создаем директорию git_repo_2
mkdir git_repo_2

# Переходим в созданную директорию
cd git_repo_2

# Инициализируем Git-репозиторий
git init

# Создаем файл numbers.txt с содержимым
echo -e "4\n5\n6\n7" > numbers.txt

# Добавляем файл в список отслеживаемых
git add numbers.txt

# Выполняем коммит
git commit -m "Добавлен файл numbers.txt с числами 4, 5, 6, 7"