from django.http import JsonResponse
from ..views.base import BaseUsersAuthorization


class UserAuthorization(BaseUsersAuthorization):

    def post(self, request):
        user_status = self.user_authorization_controller(request)
        self.logger(request, user_status['status'])
        return JsonResponse({"status": user_status['status'], 'data': user_status['data']})
