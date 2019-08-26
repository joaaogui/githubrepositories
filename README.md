# githubrepositories
A simple django application that shows your repositories, and lets you change it's tags.  

[![Build Status](https://travis-ci.org/joaaogui/githubrepositories.svg?branch=master)](https://travis-ci.org/joaaogui/githubrepositories)

[![Maintainability](https://api.codeclimate.com/v1/badges/5cddc21c068762f838fc/maintainability)](https://codeclimate.com/github/joaaogui/githubrepositories/maintainability)

# Requirements

* Virtualenv and/or Docker

# Installation

```bash
$ git clone https://github.com/joaaogui/githubrepositories.git
$ cd githubrepositories
$ workon <MyVirtualEnv>
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser (Necessary for github oauth configuration)
$ python manage.py runserver
```

# Adding enviroment variables

To customize some enviroment variables create the file  `.env` on `./githubrepositories/` with the following information:

```
SECRET_KEY = <your_secret_key>
DEBUG = True
ALLOWED_HOSTS = ['allowed_host1', 'allowed_host2']
```

# Third-Party Libraries

In this project, there are a few oflibraries that was used: 

* Allauth (For oauth authorization flow)
* Django-Taggit (For tag management)


# Database Migration and user creation

Basic django migrations and user creation. Note: The super user is necessary for the right configuration of allauth

```bash
$ python manage.py migrate
$ python manage.py createsuperuser
```


# Starting the development server

```bash
$ python manage.py runserver
```


# Admin interface


The admin interface should be available at: http://127.0.0.1:8000/admin. 

Now you can log in using the user credentials that were create at # Database Migration and user creation.

Now you should follow the following tutorial for setting up the Oauth using allauth with your APP Information(Redirect_url, Client_id, Client_secret)


Once you're done, the main page is at http://127.0.0.1:8000/.

# Running tests

```bash
$ workon <MyVirtualEnv>
$ pytest
```
