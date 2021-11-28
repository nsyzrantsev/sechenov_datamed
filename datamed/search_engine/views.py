from django.shortcuts import render
import json
from .services import get_articles_from_db, save_articles_in_db
from .forms import AddSearchForm
from django.views.generic import FormView


class SearchPubmedView(FormView):
    template_name = 'search_engine/search_pubmed.html'
    search_form = AddSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск в pubmed'
        return context

    def get(self, request, *args, **kwargs):
        form = self.search_form(request.GET)
        if form.is_valid():
            query = form['user_query'].value()
            data_list = get_articles_from_db(query)
            return render(request, self.template_name,
                          {'form': form,
                           'db_data_list': json.dumps(data_list)})
        return render(request, self.template_name, {'form': self.search_form})

    def post(self, request, *args, **kwargs):
        form = self.search_form(request.POST)
        if form.is_valid():
            query_text = form['user_query'].value()
            # Check is a number field is empty or not
            save_articles_in_db(query_text)
            data_list = get_articles_from_db(query_text)
            return render(request, self.template_name,
                          {'form': form,
                           'db_data_list': json.dumps(data_list)})
        return render(request, self.template_name, {'form': self.search_form})


class SearchLocalView(SearchPubmedView):
    template_name = 'search_engine/search_local.html'
    search_form = AddSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск в локальной базе данных'
        return context

    def get(self, request, *args, **kwargs):
        form = self.search_form(request.GET)
        if form.is_valid():
            query = form['user_query'].value()
            data_list = get_articles_from_db(query)
            return render(request, self.template_name,
                          {'form': form,
                           'db_data_list': json.dumps(data_list)})
        return render(request, self.template_name, {'form': self.search_form})
