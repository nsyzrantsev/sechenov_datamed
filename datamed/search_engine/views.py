from django.shortcuts import render
import json
from .services import get_articles_from_db


def index(request):
    query = request.GET.get('text')
    html_context = dict()
    if request.method == "GET":
        if query is not None:
            data_list = get_articles_from_db(query)
            html_context = {'data_list': json.dumps(data_list)}
    return render(request, 'search_engine/search_with_grid.html', html_context)