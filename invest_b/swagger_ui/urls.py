

from .views import yaml_to_html

try:
    from django.urls import path

    urlpatterns = [
        path('api/swagger', yaml_to_html, name="api-swagger"),
    ]
except:
    from django.conf.urls import url

    urlpatterns = [
        url(r'^api/swagger/', yaml_to_html, name="api-swagger"),
    ]
