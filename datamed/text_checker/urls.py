from django.urls import path

from .views import *

urlpatterns = [
    path('checktext/', index, name='index'),
]