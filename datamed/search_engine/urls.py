from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='search_page'),  # http://127.0.0.1:8000/
]