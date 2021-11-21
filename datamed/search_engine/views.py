from django.shortcuts import render
import json
from .services import get_articles_from_db, save_articles_in_db
from .forms import AddSearchForm
from django.views.generic import FormView


class SearchView(FormView):
    template_name = 'search_engine/search_with_grid.html'
    search_form = AddSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск в базе данных'
        return context

    def get(self, request, *args, **kwargs):
        form = self.search_form(request.GET)
        if form.is_valid():
            query = form['user_query'].value()
            data_list = get_articles_from_db(query)
            return render(request, 'search_engine/search_with_grid.html',
                          {'form': form,
                           'db_data_list': json.dumps(data_list)})
        return render(request, 'search_engine/search_with_grid.html', {'form': self.search_form})

    def post(self, request, *args, **kwargs):
        form = self.search_form(request.POST)
        if form.is_valid():
            query = form['user_query'].value()
            save_articles_in_db(query)
            data_list = get_articles_from_db(query)
            return render(request, 'search_engine/search_with_grid.html',
                          {'form': form,
                           'db_data_list': json.dumps(data_list)})
        return render(request, 'search_engine/search_with_grid.html', {'form': self.search_form})
