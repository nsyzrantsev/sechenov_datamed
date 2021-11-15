from .models import *


def get_articles_from_db(query):
    db_objs = DdiXFact.objects.filter(sentence_txt__icontains=query)
    return list(db_objs.values())

