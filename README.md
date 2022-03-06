## Инструкция запуска приложения

1. Загрузить дамп базы данных в базу данных ```meta1```
2. Действия в корневой папке проекта - ```~\sechenov_datamed\ ```:
   1. Создать виртуальную среду в корневой папке проекта. Ввести в командной строке в корневой папке проекта: ```python3 -m venv```
   2. Активировать виртуальную среду коммандой: ```venv\Scripts\activate.bat```:
   3. установка requirement.txt ```pip install -r requirements.txt```
3. Действия в корневой папке django проекта - ```~\sechenov_datamed\datamed\ ```:
   1. Добавить файл ```connection.cnf```, если этого файла нет:
      ```
      [client]
      database = meta1
      user = root1
      password = root1
      default-character-set = utf8
      ```
   2. Запустить проект командой: ```python manage.py runserver```


