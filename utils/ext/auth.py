from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from utils import return_code
import jwt

class CurrentUser(object):
    def __init__(self, user_id, username, exp):
        self.user_id = user_id
        self.username = username
        self.exp = exp

class JwtTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # 读取用户jwt
        # token = request.query_params.get("token")
        # 去请求头获取token  Authorization

        token = request.META.get("HTTP_AUTHORIZATION")

        if not token:
            raise AuthenticationFailed({"code": return_code.AUTH_FAILED, "error": "认证失败"})
        # jwt token校验
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, ["HS256"])
            return CurrentUser(**payload), token
        except Exception as e:
            raise AuthenticationFailed({"code": return_code.AUTH_FAILED, "error": "认证失败"})

    def authenticate_header(self, request):
        return "Bearer realm='API'"