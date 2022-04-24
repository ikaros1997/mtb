from django.urls import path
from rest_framework import routers
from .views import account

router = routers.SimpleRouter()

urlpatterns = [
    path("auth/", account.AuthView.as_view()),
    path("test/", account.TestView.as_view()),
]

urlpatterns += router.urls

