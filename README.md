# blogicum project

## Описание
Это сайт, на котором пользователь может создать свою страницу и публиковать на ней сообщения («посты»). 
Для каждого поста указывается категория — например «путешествия», «кулинария» или «python-разработка», а также опционально локация, с которой связан пост, например «Остров отчаянья» или «Караганда». 
Пользователь может перейти на страницу любой категории и увидеть все посты, которые к ней относятся.
Пользователи могут заходить на чужие страницы, читать и комментировать чужие посты.
Для своей страницы автор может задать имя и уникальный адрес.


## Как запустить проект:

* Выполнить последовательно в командной строке:
  - Клонировать репозиторий:
    ```
    git clone https://github.com/acunathink/acunas_blogicum_project.git && cd acunas_blogicum_project
    ```

  - Cоздать виртуальное окружение:
    * <sub>linux/macos:</sub>
    ```
    python3 -m venv venv
    ```
    * <sub>windows:</sub>
    ```
    python -m venv venv
    ```

  - Aктивировать виртуальное окружение:
    * <sub>linux/macos:</sub>
    ```
    source venv/bin/activate
    ```
    * <sub>windows:</sub>
    ```
    source venv/scripts/activate
    ```

  - Установить зависимости из файла requirements.txt:
    ```
    pip install -r requirements.txt
    ```

  - Выполнить миграции и запустить проект:
    * <sub>linux/macos:</sub>
    ```
    cd blogicum && python3 manage.py migrate && python3 manage.py runserver
    ```

    * <sub>windows:</sub>
    ```
    cd blogicum && python manage.py migrate && python manage.py runserver
    ```
