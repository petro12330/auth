import re
from .models import User
from .modules.hash_password import hash_user_password


def data_analizator_token(request_data: dict) -> dict:
    if 'access_token' in request_data and 'refresh_access_token' in request_data:

        return {"status": "Success"}
    else:
        return {"status": "Bad Request"}


def data_analizator(request_data: dict) -> dict:
    data = {}
    if "login" in request_data and 'password' in request_data:
        data['login'] = request_data['login']
        data['password'] = request_data['password']

        return {"status": "Success", 'data': data}
    else:
        return {"status": "Введите логин и пароль"}


def validator(data: dict) -> dict:
    error = False
    message = 'Success'
    password = data['password']
    login = data['login']
    res = [re.search(r"[a-z]", password), re.search(r"[A-Z]", password), re.search(r"[0-9]", password),
           re.search(r"\W", password)]
    if not all(res) or len(password) < 8:
        error = True
        message = 'Слишком простой пароль'
        return {'error': error, 'message': message}
    try:
        user = User.objects.get(login=login)
        error = True
        message = 'Логин занят('
        return {'error': error, 'message': message}
    except:
        return {'error': error, 'message': message}


def validator_user(data: dict) -> dict:
    error = False
    message = 'Success'
    password = data['password']
    h_password = hash_user_password(password)
    login = data['login']
    try:
        user = User.objects.get(login=login)
    except:
        message = 'Неправильный логин или пароль'
        error = True
        return {'error': error, 'message': message}
    if h_password == user.password:
        return {'error': error, 'message': message, 'uuid': user.uuid}
    message = 'Неправильный логин или пароль'
    error = True
    return {'error': error, 'message': message}
