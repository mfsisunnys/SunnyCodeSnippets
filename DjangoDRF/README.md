# Pet Meetup

Pet Meetup is a platform where pet owners can find other pet owners or pet lovers in their area and schedule a meetup.

---

## How it works

- User can register and login.
- User can create a pet profile.
- User can create a meetup.
- User can search for other pet owners in their area.
- User can communicate with other pet owners through our chat feature.
- User can post a picture of their pet.

---

## Technologies

1. Django
2. Django Rest Framework
3. Django Channels
4. PostgreSQL
5. PyTest
6. React

## Other Details
- Used django-channels for chat feature.
- Used JWT for authentication.
- Used AWS S3 for storing media files.
- Used SES for sending emails.
- Used Twilio for sending SMS.
- Used AWS for infrastructure.

---


## Setup
- Add .env file with specific credentials ( refer to sample.env file )

```
git clone projecturl
cd projectname
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

## Note :
Shared here a snapshot (chat feature) of the whole project.
