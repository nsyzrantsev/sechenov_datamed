from django.shortcuts import render
from .models import *
import json
from .services import *


def index(request):
    return render(request, 'pubmed_bert/index.html', {})
