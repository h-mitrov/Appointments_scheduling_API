# Appointments scheduler (a Django web app + API)

This is a web app for scheduling appointments (e.g. medical). It has an API, as well as graphic user interface.

Any feedback or advise would be really appreciated.

## Demo
Feel free to try out the API — go to https://appointerer.herokuapp.com/

To use the graphic interface, login via https://appointerer.herokuapp.com/admin

## Overview
Here's an overview of the app:
![App overview](https://i.ibb.co/Jvsg25X/image.png)

And this is overview of it's main entities:
![Main entities](https://i.ibb.co/Z81SPRs/image.png)

## Requirements
* Python 3.10.0
* Django 4.0.5
* Django REST Framework 3.13.1

## Structure / Endpoints
For Appointments, Workers, Locations, Schedules and Users, we have endpoints like `workers`, so we can use the following URLS - `/workers/` and `/workers/<id>` for collections and elements, respectively:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`workers` | GET | READ | Get all workers
`workers/<id>` | GET | READ | Get a single worker
`workers`| POST | CREATE | Create a new worker
`workers/<id>` | PUT | UPDATE | Update a worker
`workers/<id>` | DELETE | DELETE | Delete a worker

## How to use this API
You can test this Appointment booking API using [Postman](https://www.postman.com/) or any other tool you prefer.

### For non-authenticated users
Non-authenticated users can get a list of all workers (specialists), check whether they are available at a given date and time or not.
Also, they can filter workers by specialty, for example:

```
https://appointerer.herokuapp.com/filter-specialists/?date=2022-06-28&specialty=Therapist
```
Output:
```
{
        "pk": 1,
        "first_name": "Ivan",
        "last_name": "Kovalenko",
        "phone": "380993150001",
        "specialty": "Therapist",
        "available_slots": [
            "11:00",
            "12:00",
            "13:00",
            "14:00"
        ],
        "work_schedule": [
            {
                "pk": 1,
                "weekday": "Monday",
                "from_hour": "07:00:00",
                "to_hour": "10:00:00"
            },
            {
                "pk": 3,
                "weekday": "Tuesday",
                "from_hour": "09:00:00",
                "to_hour": "15:00:00"
            }
        ]
    }
```
### For authenticated users

Other features are available only to authenticated users. If you try this without your credentials:
```
https://appointerer.herokuapp.com/appointments/
```
You get:
```
{
    "detail": "Authentication credentials were not provided."
}
```
Instead, you need to pass your `username` and `password` as a form data via POST request to this endpoint:
```
https://appointerer.herokuapp.com/auth/
```
You'll get the tokens:
```
{
    "refresh": "eyJ0eMaiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1NjU2ODQyOSwiaWF0IjoxNjU2Mzk1NjI5LCJqdGkiOiJmZGMxMWQ1ZTI1NTM0ZjQ1YTk4MGExYzI0ZTg5ZTdjYSIsInVzZXJfaWQiOjF9.xIOxthD1sZEtYK755-wnBqE7DW6rw8h9Zn9y_3K3C5s",
    "access": "eyJ0eMaiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU2NDEzNjI5LCJpYXQiOjE2NTYzOTU2MjksImp0aSI6IjZkNmQxMmU0MzM0NTQ0MTM5MTY1NzBjNmExMzM0YzEwIiwidXNlcl9pZCI6MX0.eqxmcXFE1tnRVaghdcjPfSdSnNM_d4cJcyrvUxGvSZI"
}
```
We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after some time (5 hours by default). We can use the `refresh` token to request a new access token.
You'll need to pass the `refresh` as POST form-data parameter.
```
https://appointerer.herokuapp.com/auth/token/
```
Make sure to include the access token to the every next request. You will be able to perform CRUD operations with Workers, Locations, Schedules, Appointments, etc.


### Superuser rights
If you're the superuser, you will be able to create new Administrators (they have the rights only to create, update and delete Appointments).
For this, use the endpoint `workers/` or `workers/<id>`.


## How to run it locally
To run this app locally, stick to the following guide:

0. Clone the project from GitHub using whenever method you prefer. For example, if you're using PyCharm, here's a [guide on how to do this](https://www.jetbrains.com/help/pycharm/set-up-a-git-repository.html#clone-repo).
1. Create a virtual environment, for example using Virtualenv.
Type the following command to your terminal:
```bash
    virtualenv venv             
```
2. Activate the virtual environment:
```bash
    venv/scripts/activate              
```
3. Install the dependencies from the requirements.txt:
```bash
    pip install -r requirements.txt              
```
4. Make database migrations:
```bash
    python manage.py makemigrations
    python manage.py migrate
```
5. Create superuser:
```bash
    python manage.py createsuperuser
```
6. Run the app:
```bash
    python manage.py runserver
```