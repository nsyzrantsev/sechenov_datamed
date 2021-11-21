from .models import DdiXFact, DdiFact, Task, Source
from Bio import Entrez, Medline
import sys

from pathlib import Path

path_to_bert = str(Path.joinpath(Path(__file__).resolve().parent.parent, 'BERT_core'))
sys.path.append(path_to_bert)

from BERT_core.main import main as bert_prediction


# Get articles from DdiFact table
def get_articles_from_db(query):
    db_objs = DdiFact.objects.filter(sentence_txt__icontains=query)
    return list(db_objs.values())


# Save BERT predictions in DdiFact table
def save_articles_in_db(query):
    xml_list = get_xml_list(query, 1, 'pubmed')
    articles = get_articles_parameters(xml_list, ['PMID', 'AB'])
    task = Task(source_id=Source.objects.get(source_id=1),
                query_text=query)
    task.save()
    for article in articles:
        article = add_predicted_values(article)
        if not DdiFact.objects.filter(id_doc=article.get('PMID')).exists():
            ddi_fact = DdiFact(id_task=task,
                               id_doc=article.get('PMID'),
                               sentence_txt=article.get('AB'),
                               parsing_txt=article.get('parsing_txt'),
                               numb_sentence_in_doc=0,
                               ddi_type=article.get('ddi_type'))
            ddi_fact.save()


# Return xml list of articles by user query
def get_xml_list(query, articles_number, database_name):
    Entrez.email = 'nicksyz13@gmail.com'
    # Searches and retrieves primary IDs
    handle = Entrez.esearch(
        db=database_name,
        sort='relevance',
        term=query,
        pagination='3',
        retmax=articles_number
    )
    id_list = Entrez.read(handle)["IdList"]
    # Retrieve records in the requested format from a list of one or more primary IDs
    articles_handles = Entrez.efetch(db=database_name, id=id_list, rettype="medline", retmode="text")
    articles = Medline.parse(articles_handles)
    # Generation of list of the articles
    articles_result = []
    for article in articles:
        articles_result.append(article)
    return articles_result


# Return list of articles with chose parameters
# Such as: Title, Abstract, Authors etc
def get_articles_parameters(xml_list, parameters):
    articles = []
    for xml in xml_list:
        article = dict()
        for parameter in parameters:
            if xml.get(parameter) is not None:
                article[parameter] = xml.get(parameter)
            else:
                return []
        articles.append(article)
    return articles


# Predict tokens for words in articles texts,
# drug-drug interaction
# and add it to article dict
def add_predicted_values(article):
    prediction = bert_prediction(article.get('AB'))
    article['parsing_txt'] = prediction[0]['text_after_bert']
    article['ddi_type'] = prediction[0]['ddi']
    return article
