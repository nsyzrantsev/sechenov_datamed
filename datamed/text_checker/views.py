from django.shortcuts import render
import json
from .forms import AddTextareaForm
import sys
from pathlib import Path

path_to_bert = str(Path.joinpath(Path(__file__).resolve().parent.parent, 'BERT_core'))
sys.path.append(path_to_bert)

from BERT_core.main import main


def index(request):
    if request.method == "GET":
        form = AddTextareaForm(request.GET)
        if form.is_valid():
            query = form['user_text'].value()
            prediction = main([query])
            return render(request, 'text_checker/text_area.html',
                          {'form': form,
                           'title': 'Анализ текста',
                           'prediction': json.dumps(prediction)})
    else:
        form = AddTextareaForm()
    return render(request, 'text_checker/text_area.html', {'form': form,
                                                           'title': 'Анализ текста'})
