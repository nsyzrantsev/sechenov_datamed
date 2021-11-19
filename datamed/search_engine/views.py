from django.shortcuts import render
import json
from .services import get_articles_from_db
from .forms import AddSearchForm


def index(request):
    if request.method == "GET":
        form = AddSearchForm(request.GET)
        if form.is_valid():
            query = form['user_query'].value()
            data_list = get_articles_from_db(query)
            return render(request, 'search_engine/search_with_grid.html',
                          {'form': form,
                           'title': 'Поиск в базе данных',
                           'db_data_list': json.dumps(data_list)})
    else:
        form = AddSearchForm()
    return render(request, 'search_engine/search_with_grid.html', {'form': form,
                                                                   'title': 'Поиск в базе данных'})
