from rest_framework import serializers
# Подключаем модель user
from .models import User
from django.contrib.auth import authenticate

class UserRegistrSerializer(serializers.ModelSerializer):
    # Поле для повторения пароля
    password2 = serializers.CharField()

    # Настройка полей
    class Meta:
        # Поля модели которые будем использовать
        model = User
        # Назначаем поля которые будем использовать
        fields = ['email', "login", 'password', 'password2', "phone"]

    # Метод для сохранения нового пользователя
    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = User(
            email=self.validated_data['email'],  # Назначаем Email
            login=self.validated_data["login"],
            phone=self.validated_data["phone"]
        )
        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        if password != password2:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя
        return user


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['login', 'password']

    def validate(self, attrs):
        """Проверка на существование юзера в базе"""
        try:
            user_ex = User.objects.get(login=attrs["login"])
        except:
            return "ERROR"

        """Проверка на правильность логина и пароля, подтверждение юзера"""
        user = authenticate(login=attrs['login'], password=attrs['password'])

        if not user and not user_ex:
            raise serializers.ValidationError({"resultCode": 1, "message": 'Incorrect login or password.'})

        if not user_ex.is_active:
            raise serializers.ValidationError({"resultCode": 1, "message": "User is disabled."})

        return {'user': user, "password": attrs['password']}

class RegConfirmRepeatSerializer(serializers.Serializer):
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ['email']

    def validate(self, *args, **kwargs):
        """Проверка на существование юзера в базе"""
        try:
            user = User.objects.get(email=self.validated_data["email"])
            print(user)
        except:
            return "ERROR"

        return user