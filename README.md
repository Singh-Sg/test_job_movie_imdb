# Assignment to show movies list from wikidata.org

## Description

1. Firstly, we recover some raw data from https://query.wikidata.org/
2. Store that data in database.
3. Then we display some tables of the data stored in our database by using- Flask

## How to start

Project is ready to run (with some requirements). You need to clone, create a virtual environment and run:

```sh
$ mkdir Project
$ cd Project
$ git clone git@github.com:xen/flask-project-template.git .
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install requirements.txt
$ flask db init
$ flask db migrate -m "Initial migration"
$ flask db upgrade
$ python -m flask run
```

Open http://127.0.0.1:5000/, customize project files and **have fun**.

At first, their is not data in our database. To store some data you have to click on the option **Refresh Database** so it take few second and it will iterate all the movies from the wikidata which is released after 2013.


