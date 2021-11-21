from django.shortcuts import render
import json
from .forms import AddTextareaForm
from django.views.generic import FormView
import sys
from pathlib import Path

path_to_bert = str(Path.joinpath(Path(__file__).resolve().parent.parent, 'BERT_core'))
sys.path.append(path_to_bert)

from BERT_core.main import main as bert_prediction


class TextareaView(FormView):
    template_name = 'text_checker/text_area.html'
    textarea_form = AddTextareaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Анализ текста'
        return context

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            form = self.textarea_form(request.GET)
            if form.is_valid():
                query = form['user_text'].value()
                prediction = bert_prediction([query])
                return render(request, self.template_name, {'form': form, 'prediction': json.dumps(prediction)})
        return render(request, self.template_name, {'form': self.textarea_form})
