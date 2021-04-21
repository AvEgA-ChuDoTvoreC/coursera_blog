# coursera_blog

tmp project to learn **Django + Bootstrap** integration

<br>

## Installation

Clone the repo:
```bash
$ git clone https://github.com/AvEgA-ChuDoTvoreC/coursera_blog.git
$ cd coursera_blog
```
Set up virtual environment:
```bash
$ virtualenv -p 3.9.2 web
$ source web/bin/activate
$ pip install -r requirements.txt
```
Run the server:
```bash
$ python manage.py runserver
```

<br>

Need database migrations?
```bash
commands:
    - makemigrations
    - migrate
    - sqlmigrate
    - showmigrations
$ python manage.py makemigrations
$ python manage.py migrate
```

Need admin panel?
```bash
$ python manage.py createsuperuser --username=USERNAME --email=EMAIL

http://127.0.0.1:8000/admin/
```

<br>

## Check work

Start with:
```
Blog pages:
    http://127.0.0.1:8000/core/index3/
    http://127.0.0.1:8000/core/index{N}/

API:
    add goods (POST):
        http://127.0.0.1:8000/api/v1/goods/
            {"title": "Chedder", "description": "good cheese", "price": 70}
    add review (POST):
        http://127.0.0.1:8000/api/v1/goods/1/reviews/
            {"text": "Best. Cheese.", "grade": 9}
    check (GET):
        http://127.0.0.1:8000/api/v1/goods/1/

Auth + send form:
    http://127.0.0.1:8000/formdummy/form/
```

Problems?
```
Use curl or postman
$ curl -v -H "Content-Type: application/json" -X GET http://127.0.0.1:8000/api/v1/goods/1/
```

<br>

TODO:
 - [ ] DataBase
 - [ ] Logout page

<br>

## Visual Examples of StackOverflow mockup


![stackoverflow_mockup](https://github.com/AvEgA-ChuDoTvoreC/coursera_blog/blob/main/core/static/core/img/stackoverflow_mockup.png)

![stackoverflow_mockup2](https://github.com/AvEgA-ChuDoTvoreC/coursera_blog/blob/main/core/static/core/img/auth_post_form.png)


## 


