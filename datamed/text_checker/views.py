from django.shortcuts import render
from .models import *
import json
from .services import *


def index(request):
    return render(request, 'text_checker/index.html', {})
