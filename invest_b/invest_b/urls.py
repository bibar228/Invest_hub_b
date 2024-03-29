"""
URL configuration for invest_b project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, \
    TokenRefreshSlidingView

from swagger_ui.views import view_swagger_json

from analize.views import SiggsViewSet
from users.views import RecoveryPassword
from users.views import ChangePassword
from users.views import UserView
from users.views import logout_view
from users.views import home
from users.views import RegistrUserView, LoginView, register_confirm, RegConfirmRepeat, recovery_password_confirm, \
    refresh_tokens, logout



urlpatterns = [
    path('', include('swagger_ui.urls')),
    path('api/swagger_json/', view_swagger_json),
    path('admin/', admin.site.urls),
    path('api/auth/registr/', RegistrUserView.as_view(), name='registr'),
    path("api/auth/log/", LoginView.as_view()),
    path('api/auth/logout/', logout, name='logout_token'),
    path("api/auth/confirmed/<token>/", register_confirm, name="register_confirm"),
    path("api/auth/confirm_repeat/", RegConfirmRepeat.as_view()),
    path('api/token/refresh/', refresh_tokens, name='token_refresh'),
    #path('api/auth/logout/', logout_view, name='logout'),
    path("api/auth/change_password/", ChangePassword.as_view()),
    path("api/auth/recovery_password/", RecoveryPassword.as_view()),
    path("api/auth/recovery_password/<token>/", recovery_password_confirm, name="recovery_password_confirm"),
    path("a/", UserView.as_view({'get': 'list'}), name='for_tests_back'),
    path("", home, name='zaglushka'),
    path('api/siggs', SiggsViewSet.as_view({'get': 'list'}), name='siggs')
    ]
