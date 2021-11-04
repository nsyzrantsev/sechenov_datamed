from django.shortcuts import render
from .models import *


def index(request):
    query = request.GET.get('q')
    if request.method == "GET":
        if query is not None:
            query = request.GET.get('q')
            db_objs = DdiXFact.objects.filter(sentence_txt__icontains=query)
            data_list = list(db_objs.values())
            return render(request, 'search_engine/index.html', {'data_list': data_list})
    return render(request, 'search_engine/index.html', {})
