from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate

class CaptureIPAddressMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        token_authentication = TokenAuthentication()
        try:
            user, _ = token_authentication.authenticate(request)
            if user:
                user.ip_address = ip_address
                user.save()
        except:
            pass
