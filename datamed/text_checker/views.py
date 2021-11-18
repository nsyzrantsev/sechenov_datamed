from django.shortcuts import render
import sys
sys.path.append('../datamed/BERT_core/')
from BERT_core.main import main


def index(request):
    prediction = {}
    article_text = request.GET.get('text')
    if request.method == "GET":
        if article_text is not None:
            prediction = main([article_text])
    return render(request, 'text_checker/index.html', {'prediction': prediction})
