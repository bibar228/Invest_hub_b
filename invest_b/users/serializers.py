from rest_framework import serializers
# Подключаем модель user
from .models import User
from django.contrib.auth import authenticate

class UserRegistrSerializer(serializers.ModelSerializer):
    # Поле для повторения пароля
    password2 = serializers.CharField(
        max_length=32,
        min_length=4,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    # Настройка полей
    class Meta:
        # Поля модели которые будем использовать
        model = User
        # Назначаем поля которые будем использовать
        fields = ['email',  'password', 'password2', "phone", "token"]

    # Метод для сохранения нового пользователя
    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = User(
            email=self.validated_data['email'],
            phone=self.validated_data["phone"]
        )
        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        if password != password2:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({"resultCode": 1, "message": "Passwords don't match"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        """Проверка на существование юзера в базе"""
        try:
            user_ex = User.objects.get(email=attrs["email"])
        except:
            return "ERROR"

        """Проверка на активацию юзера"""
        if not user_ex.is_active:
            raise serializers.ValidationError({"resultCode": 1, "message": "User is disabled."})

        """Проверка пароля"""
        user = authenticate(email=attrs['email'], password=attrs['password'])

        if user is None:
            raise serializers.ValidationError({"resultCode": 1, "message": 'Incorrect password.'})

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
        except:
            return "ERROR"

        return user