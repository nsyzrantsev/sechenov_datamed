from .models import DdiFact, Task, Source, DrugLink
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
def save_articles_in_db(query, articles_num=5):
    articles = get_xml_list(query, articles_num+20, 'pubmed')
    task = Task(source_id=Source.objects.get(source_id=1),
                query_text=query)
    task.save()
    for article in articles:
        if article.get('AB') is not None and article.get('PMID') is not None:
            if articles_num > 0 and not DdiFact.objects.filter(id_doc=article.get('PMID')).exists():
                article_after_bert = bert_prediction(article.get('AB'))
                articles_num -= 1  # Counter of the number of articles actually found
                for sentence in article_after_bert:
                    ddi_fact = DdiFact(id_task=task,
                                       id_doc=article.get('PMID'),
                                       sentence_txt=sentence.get('text_before_bert'),
                                       parsing_txt=sentence.get('text_after_bert'),
                                       numb_sentence_in_doc=sentence.get('sentence_number'),
                                       ddi_type=sentence.get('ddi'))
                    ddi_fact.save()
                    if len(sentence.get('drugs')) > 0:
                        for drug in sentence.get('drugs'):
                            drug_link = DrugLink(id_fact=ddi_fact,
                                                 drug_name=drug)
                            drug_link.save()


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
