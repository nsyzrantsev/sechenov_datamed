from django.urls import path

from .views import SearchPubmedView, SearchLocalView

urlpatterns = [
    path('', SearchPubmedView.as_view(), name='search_pubmed_page'),  # http://127.0.0.1:8000/
    path('local/', SearchLocalView.as_view(), name='search_local_page'),  # http://127.0.0.1:8000/local
]