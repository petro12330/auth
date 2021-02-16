from rest_framework.views import APIView

from django.conf import settings
from ..modules.user_auth import *
from ..modules.hash_password import hash_user_password
from ..validators import validator, data_analizator, data_analizator_token, validator_user
from ..models import User

import logging

auth_logger = logging.getLogger(__name__)


class BaseMethods(APIView):
    """Методы, используемые во всех классах"""

    access_token_ttl = settings.USER_ACCESS_TOKEN_TTL
    refresh_token_ttl = settings.USER_REFRESH_TOKEN_TTL
    token_size = settings.USER_TOKEN_SIZE

    def logger(self, request, response):
        auth_logger.info(
            f'{request.method} - {request.build_absolute_uri()}\n\nQuery Params\n{request.GET}\n\nHeaders\n{request.headers}\n\nData:\n{request.data}\n\nResponse: {response}')

    def get_request_data(self, request):
        data = request.data
        return data


class BaseUsersAuthorization(BaseMethods):
    """Классы для работы с Авторизацией пользователей"""

    def user_authorization_controller(self, request):

        request_data = self.get_request_data(request)
        data_status = data_analizator(request_data)

        if data_status["status"] == "Success":
            data = data_status['data']
            valid = validator_user(data)
            if valid['error']:
                return {"data": valid['message'], "status": 400}

            tokens = crate_user_tokens(self.access_token_ttl, self.token_size, self.refresh_token_ttl,
                                       user_uuid=valid['uuid'])

            return {"data": tokens, 'status': 201}
        else:
            return {"data": data_status["status"], "status": 400}


class BaseUserRegistration(BaseMethods):
    """Для регистрации пользователей"""
    error_messages = {}

    def registration(self, request):

        request_data = self.get_request_data(request)
        data_status = data_analizator(request_data)
        if data_status["status"] == "Success":

            data = data_status['data']
            valid = validator(data)
            if valid['error']:
                return {"data": valid['message'], "status": 400}
            data['password'] = hash_user_password(data['password'])
            new_user = User(login=data['login'], password=data['password'], role='user')
            new_user.save()
            return {"data": data_status["status"], 'status': 201}
        else:
            return {"data": data_status["status"], "status": 400}


class BaseUserSession(BaseMethods):
    """Сессия"""

    def session_controller(self, request):
        request_data = self.get_request_data(request)
        data_status = data_analizator_token(request_data)
        if data_status["status"] == "Success":
            data = verification_user_token(request_data)
            if data["status"] == "Success":
                return {"data": 'Success', "status": 201}
            elif data["status"] == 'Your access_token was burned':
                tokens = update_user_tokens(request_data['refresh_access_token'],self.access_token_ttl, self.token_size, self.refresh_token_ttl)
                return {"data": tokens, 'status': 201, 'massage': data['status']}
            return {"data": 'Bad Request', "status": 400}
        return {"data": data_status["status"], "status": 400}
