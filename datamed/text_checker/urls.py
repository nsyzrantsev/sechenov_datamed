from django.urls import path

from .views import TextareaView

urlpatterns = [
    path('', TextareaView.as_view(), name='check_page'),  # http://127.0.0.1:8000/text_check/
]
