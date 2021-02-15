from django.http import JsonResponse

from ..views.base import BaseUserSession


class UserSession(BaseUserSession):

    def post(self, request):
        user_status = self.session_controller(request)
        self.logger(request, user_status['status'])
        return JsonResponse({"status": user_status['status'], 'data': user_status['data']})
