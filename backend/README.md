# Django back-end

## Available Scripts

In the project directory, you can run:

### `./run.sh ` or `python3 manage.py runserver`

To start the back-end server on [http://localhost:8000/](http://localhost:8000/)

### `python3 manage.py makemigrations`

To creating new migrations based on the changes you have made to your models.

### `python3 manage.py migrate`

To apply migrations.

### `python3 manage.py dumpdata --indent=2 -o dummy.json webbot`

To dump dummy data from SQLite db

### `python3 manage.py loaddata dummy.json`

To load data to SQLite db from dummy.json

### `python3 manage.py flush`

To clear db

## Other

### Django admin

Django admin interface: [http://localhost:8000/admin/](http://localhost:8000/admin/)

### Django REST framework

Django REST framework interface: [http://localhost:8000/api/](http://localhost:8000/api/)