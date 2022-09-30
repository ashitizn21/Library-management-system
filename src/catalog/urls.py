from django.urls import re_path

from .views import demo

app_name = 'catalog'

urlpatterns = [
    re_path(r'^$', demo, name='demo'),
]