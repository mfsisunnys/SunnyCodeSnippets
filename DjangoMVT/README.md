# KOS Meetup

KOS meetup is a platform where users can sumbit research papers and can also review other research papers and can also give ratings to the research papers.

---

## How it works

- User can register and login.
- User can buy membership.
- User can submit research paper.
- User can review other research papers.
- User can give ratings to the research papers.

---

## Technologies

1. Django
2. Django Rest Framework
3. Django Channels
4. MySQL
5. PyTest

## Other Details

- Used django-channels for notifications.
- Used Twilio for sending SMS.
- Used Apache as web server.

---

## Setup

- create database 'kosDB' in mysql
- use commands :

  `mysql -u root -p`

  `create database kosDB`

  `exit`


```
git clone projecturl
cd projectname
pip install -r requirements.txt
```
- add .env file with specific credentials ( refer to sample.env file )

```
python manage.py makemigrations
python manage.py migrate
```

## Note

Shared here a subset of project codebase.
