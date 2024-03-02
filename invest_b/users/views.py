import types
import uuid
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets, permissions
# Подключаем компонент для ответа
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Подключаем компонент для создания данных
from rest_framework.generics import CreateAPIView, get_object_or_404
# Подключаем компонент для прав доступа
import string
from random import choice
import jwt
from rest_framework.views import APIView
from django.shortcuts import redirect
# Подключаем модель User
from invest_b import settings
from .models import User
# Подключаем UserRegistrSerializer
from .serializers import UserRegistrSerializer, RegConfirmRepeatSerializer, UserSerializer, ChangePasswordSerializer, \
    RecoveryPasswordSerializer
from django.contrib.auth import authenticate, login
from .serializers import LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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
        if serializer.is_valid():
            token = uuid.uuid4().hex
            redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
            cache.set(redis_key, request.data["email"], timeout=settings.SOAQAZ_USER_CONFIRMATION_TIMEOUT)
            confirm_link = self.request.build_absolute_uri(
                reverse(
                    "register_confirm", kwargs={"token": token}
                )
            )
            try:
                send_mail(subject="Please confirm your registration!",
                          message=f"follow this link %s \n"
                                  f"to confirm! \n" % confirm_link,
                          from_email="sushentsevmacsim@yandex.ru",
                          recipient_list=[request.data["email"]])
            except Exception as e:
                return Response({"resultCode": 1, "message": f"There is no such mail"})

            if serializer.save() == {"resultCode": 1, "message": "Passwords don't match"}:
                return Response({"resultCode": 1, "message": "Passwords don't match"})

            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({  # Полезная информация в самом токене
                'user_id': user.id,
                'email': user.email
            })
            """Установка рефреш токена в куки"""
            response = Response()
            response.set_cookie("refresh", str(refresh), httponly=True)
            response.data = {"resultCode": 0, "message": "SUCCESS REGISTR", 'access_token': str(refresh.access_token)}
            return response

        else:  # Иначе
            # Присваиваем data ошибку
            data = {}
            data["resultCode"] = 1
            try:
                data["message"] = serializer.errors["email"]
            except:
                data["message"] = serializer.errors["phone"]
            # Возвращаем ошибку
            return Response(data)

@api_view(('GET',))
def register_confirm(request, token):
    """Если токен есть в редисе, то находим пользователя и делаем его активным, если токен протух, то ошибка и ссылка на повторный запрос токена для подтверждения"""
    redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
    buyer_info = cache.get(redis_key) or {}

    if buyer_info:
        User.objects.filter(email=buyer_info).update(is_active=True)
        return Response({"resultCode": 0, "message": "SUCCESS CONFIRM"})
    else:
        return Response({"resultCode": 1, "message": f"The confirmation time has expired",
                         "link": "link for repeat confirm - http://0.0.0.0:8000/confirm_repeat/"})


class RegConfirmRepeat(APIView):
    """Вьюха для повторной отправки ссылки на емейл для подтверждения аккаунта"""
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegConfirmRepeatSerializer

    def post(self, request):
        serializer = RegConfirmRepeatSerializer(data=request.data)
        serializer.is_valid()

        if serializer.validate(request.data) == "ERROR":
            return Response({"resultCode": 1, "message": "email address incorrect"})
        else:
            token = uuid.uuid4().hex
            redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
            cache.set(redis_key, request.data["email"], timeout=settings.SOAQAZ_USER_CONFIRMATION_TIMEOUT)
            confirm_link = self.request.build_absolute_uri(f"http://localhost:5173/auth/confirmed/{token}")

            send_mail(subject="Please confirm your registration!",
                      message=f"follow this link %s \n"
                              f"to confirm! \n" % confirm_link,
                      from_email="sushentsevmacsim@yandex.ru",
                      recipient_list=[request.data["email"]])

            return Response({"resultCode": 0, "message": "SUCCESS SEND MAIL"})


class LoginView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        """Проверка на существование юзера"""
        if serializer.validate(request.data) == "ERROR":
            return Response({"resultCode": 1, "message": f"ACCOUNT NOT REGISTER"})

        if serializer.validate(request.data) == {"resultCode": 1, "message": "User is disabled."}:
            return Response({"resultCode": 1, "message": "User is disabled."})

        if serializer.validate(request.data) == {"resultCode": 1, "message": 'Incorrect password.'}:
            return Response({"resultCode": 1, "message": 'Incorrect password.'})

        #user = serializer.validated_data['user']
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        login(request, user)
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'email': user.email
        })
        """Установка рефреш токена в куки"""
        response = Response()
        response.set_cookie("refresh", str(refresh), httponly=True)
        response.data = {"resultCode": 0, "message": f"SUCCES LOG",  'access_token': str(refresh.access_token)}
        return response

class ChangePassword(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        token = request.data["token"]
        """Проверка токена на актуальность(протух/не протух)"""
        try:
            payload_jwt = jwt.decode(
                token,
                settings.SIMPLE_JWT['SIGNING_KEY'],
                algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
        except:
            return Response({"resultCode": 1, "message": f"The Token has expired"})

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid()
        """Проверка на совпадение паролей"""
        if serializer.save(request.data) == "ERROR":
            return Response({"resultCode": 1, "message": f"Passwords don't match"})

        user = User.objects.get(id=payload_jwt["user_id"])
        user.set_password(request.data["password"])
        user.save()

        return Response({"resultCode": 0, "message": f"SUCCESS CHANGE"})

@api_view(('GET',))
def recovery_password_confirm(request, token):
    """Если токен есть в редисе, то находим пользователя и меняем пароль, если токен протух, то ошибка и ссылка на повторный запрос токена для подтверждения"""
    redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
    buyer_info = cache.get(redis_key) or {}

    if buyer_info[0]:
        user = User.objects.get(email=buyer_info[0])
        user.set_password(buyer_info[1])
        user.save()
        return Response({"resultCode": 0, "message": "SUCCESS CONFIRM"})
    else:
        return Response({"resultCode": 1, "message": f"The confirmation time has expired",
                         "link": "link for repeat confirm - http://0.0.0.0:8000/confirm_repeat/"})

class RecoveryPassword(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RecoveryPasswordSerializer

    def post(self, request):
        serializer = RecoveryPasswordSerializer(data=request.data)
        serializer.is_valid()
        """Проверка на существование юзера"""
        if serializer.validate(request.data) == "ERROR":
            return Response({"resultCode": 1, "message": f"ACCOUNT NOT REGISTER"})

        token = uuid.uuid4().hex
        new_password = ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(8, 20))
        redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
        cache.set(redis_key, [request.data["email"], new_password], timeout=settings.SOAQAZ_USER_CONFIRMATION_TIMEOUT)
        confirm_link = self.request.build_absolute_uri(
            reverse("recovery_password_confirm", kwargs={"token": token})
        )
        send_mail(subject="Please confirm recovery your password!",
                  message=f"Your new password is {new_password}\n"
                          f"follow this link %s \n"
                          f"to confirm! \n" % confirm_link,
                  from_email="sushentsevmacsim@yandex.ru",
                  recipient_list=[request.data["email"]])

        return Response({"resultCode": 0, "message": "SUCCESS SEND MAIL"})

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect("/")

def home(request):
    return HttpResponse(f"PRIVET")