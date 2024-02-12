import types
import uuid

from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.shortcuts import render

from rest_framework import status
# Подключаем компонент для ответа
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Подключаем компонент для создания данных
from rest_framework.generics import CreateAPIView, get_object_or_404
# Подключаем компонент для прав доступа

from rest_framework.views import APIView

# Подключаем модель User
from invest_b import settings
from .models import User, AuthtokenToken
# Подключаем UserRegistrSerializer
from .serializers import UserRegistrSerializer, RegConfirmRepeatSerializer
from django.contrib.auth import authenticate, login
from .serializers import LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_protect


# Создаём класс RegistrUserView

class RegistrUserView(CreateAPIView):
    # Добавляем в queryset
    queryset = User.objects.all()
    # Добавляем serializer UserRegistrSerializer
    serializer_class = UserRegistrSerializer
    # Добавляем права доступа
    permission_classes = [AllowAny]

    # Создаём метод для создания нового пользователя
    def post(self, request, *args, **kwargs):
        # Добавляем UserRegistrSerializer
        serializer = UserRegistrSerializer(data=request.data)
        # Создаём список data
        data = {}
        # Проверка данных на валидность
        if serializer.is_valid():
            # Сохраняем нового пользователя
            # Добавляем в список значение ответа True
            data['response'] = True
            # Возвращаем что всё в порядке
            token = uuid.uuid4().hex
            redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
            cache.set(redis_key, request.data["email"], timeout=settings.SOAQAZ_USER_CONFIRMATION_TIMEOUT)
            confirm_link = self.request.build_absolute_uri(
                reverse(
                    "register_confirm", kwargs={"token": token}
                )
            )
            lnk = self.request.build_absolute_uri("http://127.0.0.1:5173/auth/confirm/token")

            send_mail(subject="Please confirm your registration!",
                      message=f"follow this link %s \n"
                              f"to confirm! \n" % lnk,
                      from_email="sushentsevmacsim@yandex.ru",
                      recipient_list=[request.data["email"]])
            serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        else:  # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data)

@api_view(('GET',))
def register_confirm(request, token):
    """Если токен есть в редисе, то находим пользователя и делаем его активным, если токен протух, то ошибка и ссылка на повторный запрос токена для подтверждения"""
    redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
    buyer_info = cache.get(redis_key) or {}

    if buyer_info:
        User.objects.filter(email=buyer_info).update(is_active=True)
        return Response({"resultCode": [0], "message": ["SUCCESS CONFIRM"]})
    else:
        return Response({"resultCode": [1], "message": [f"The confirmation time has expired"],
                         "link": ["link for repeat confirm - http://0.0.0.0:8000/confirm_repeat/"]})


class RegConfirmRepeat(APIView):
    """Вьюха для повторной отправки ссылки на емейл для подтверждения аккаунта"""
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegConfirmRepeatSerializer

    def post(self, request):
        serializer = RegConfirmRepeatSerializer(data=request.data)
        serializer.is_valid()

        if serializer.is_valid():
            token = uuid.uuid4().hex
            redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
            cache.set(redis_key, request.data["email"], timeout=settings.SOAQAZ_USER_CONFIRMATION_TIMEOUT)
            confirm_link = self.request.build_absolute_uri(
                reverse(
                    "register_confirm", kwargs={"token": token}
                )
            )

            lnk = self.request.build_absolute_uri("http://127.0.0.1:5173/auth/confirm/token")

            send_mail(subject="Please confirm your registration!",
                      message=f"follow this link %s \n"
                              f"to confirm! \n" % lnk,
                      from_email="sushentsevmacsim@yandex.ru",
                      recipient_list=[request.data["email"]])
            data = {}
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)



def base(request):
    return render(request, "base.html")


class LoginView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        try:
            user = serializer.validated_data['user']
        except:
            return Response({"resultCode": [1], "message": [f"ACCOUNT DOES NOT EXIST"]})
        login(request, user)
        return Response({"resultCode": [0], "message": [f"Logged in {user}"]})