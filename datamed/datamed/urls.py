from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('search_engine.urls')),  # http://127.0.0.1:8000/
    path('text_check/', include('text_checker.urls')),  # http://127.0.0.1:8000/text_check/
    path('admin/', admin.site.urls),  # http://127.0.0.1:8000/admin
]
