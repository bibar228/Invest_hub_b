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
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import RegistrUserView, LoginView, register_confirm, RegConfirmRepeat

schema_view = get_schema_view(
    openapi.Info(
        title="Django Invest Crypto Profit IMBA 3000",
        default_version="v2",
        description="Description",
        license=openapi.License(name="BSD License"),
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('auth/registr/', RegistrUserView.as_view(), name='registr'),
    path("auth/log/", LoginView.as_view()),
    path("register_confirm/<token>/", register_confirm, name="register_confirm"),
    path("confirm_repeat/", RegConfirmRepeat.as_view())
]
