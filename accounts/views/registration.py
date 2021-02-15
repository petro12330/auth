from django.http import JsonResponse
from ..views.base import BaseUserRegistration


class UserRegistration(BaseUserRegistration):
    def post(self, request):
        user_status = self.registration(request)
        self.logger(request, user_status['status'])
        return JsonResponse({"status": user_status['status'], 'data': user_status['data']})
