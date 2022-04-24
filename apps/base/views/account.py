import jwt
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from ..serializers.account import AuthSerializer
from utils import return_code
from .. import models

class AuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # 获取用户名密码

        #  数据校验

        serializer = AuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"code": return_code.AUTH_FAILED, "detail": serializer.errors})
        # 数据库校验
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user_obj = models.UserInfo.objects.filter(username=username, password=password).first()
        if not user_obj:
            return Response({"code": return_code.VALIDATE_ERROR, "detail": "用户名或密码错误"})

        # 生成jwt token
        headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        # 构造payload
        payload = {
            'user_id': user_obj.id,
            'username': user_obj.username,
            "exp": datetime.datetime.now() + datetime.timedelta(weeks=2)
        }
        jwt_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256", headers=headers)
        return Response({"code": return_code.SUCCESS, "data": {"username": username, "token": jwt_token}})

class TestView(APIView):

    def get(self, request, *args, **kwargs):
        return Response("text")