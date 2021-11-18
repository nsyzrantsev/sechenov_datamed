from django.urls import path

from .views import index

urlpatterns = [
    path('', index, name='check_page'),  # http://127.0.0.1:8000/text_check/
]
