from django.shortcuts import render
import json

import sys
from pathlib import Path
path_to_bert = str(Path.joinpath(Path(__file__).resolve().parent.parent, 'BERT_core'))
sys.path.append(path_to_bert)

from BERT_core.main import main


def index(request):
    prediction = {}
    article_text = request.GET.get('text')
    if request.method == "GET":
        if article_text is not None:
            prediction = main([article_text])
    return render(request, 'text_checker/text_area.html', {'title': 'Анализ текста', 'prediction': json.dumps(prediction)})
