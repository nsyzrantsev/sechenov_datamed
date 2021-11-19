from django.urls import path

from .views import SearchView

urlpatterns = [
    path('', SearchView.as_view(), name='search_page'),  # http://127.0.0.1:8000/
]