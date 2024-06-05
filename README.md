# [User Management](https://github.com/Aaditya110711/user_management)

Simple starter built with Python / Django Rest / Sqlite3 and JWT Auth. The authentication flow is built with [json web tokens](https://jwt.io).

## Features:

1. **User Registration**: Users can register with a username, email, and password.
2. **User Login**: Secure login using JWT token-based authentication.
3. **Profile Update**: Authenticated users can update their profiles, including username and email.
4. **Forgot Password with Email**: Users can initiate a password reset via email with a time-limited reset link.
5. **Admin Panel**: Administrators can view a list of registered users.

## ✨ How to use the code

> 👉 **Step #1** - Clone the sources

```bash
$ git https://github.com/Aaditya110711/user_management.git
$ cd user_management
```

<br />

> 👉 **Step #2** - Create a virtual environment

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

<br />

> 👉 **Step #3** - Install dependencies using PIP

```bash
$ pip install -r requirements.txt
```

<br />

> 👉 **Step #4** - Start the API server

```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

The API server will start using the default port `8000`.

## ✨ API

For a fast set up, use this POSTMAN file: [Api_sample](https://github.com/Aaditya110711/social-networking-application/blob/master/User Management.postman_collection.json)

> **Register** - `api/user/signup/`

```
POST api/user/signup/
Content-Type: application/json

{
    "name":"test",
    "email":"test@example.com",
    "password":"pass",
    "password2":"pass",
    "tc":true
}
```


> **Login** - `api/user/login/`

```
POST /api/user/login/
Content-Type: application/json

{
    "email":"test@appseed.us",
    "password":"pass"
}
```


> **Profile Update** - `api/user/profile/update/`

```
PUT /api/user/profile/update/
Content-Type: application/json
Authorization: Bearer <token>

{
    "name":"abcd",
    "email":"test@appseed.us",
    "password":"pass"
}
```


> **Forgot Password with Email** - `api/user/request-password-reset/`

```
POST /api/user/request-password-reset/
Content-Type: application/json
Authorization: Bearer <token>

{
    "email":"test@example.com",
}
```

```
## ✨ Error Responses

Common error responses include:

- 400 Bad Request: Invalid input or request parameters.
- 401 Unauthorized: Missing or invalid authentication token.
- 403 Forbidden: Access to the requested resource is forbidden.
- 404 Not Found: Resource not found.
```



## ✨ Technologies Used

- Django: Web framework for building the application.
- Django REST Framework: Toolkit for building RESTful APIs.
- PostgreSQL: Relational database for storing user data.
- Bootstrap: Frontend framework for the admin panel UI.
