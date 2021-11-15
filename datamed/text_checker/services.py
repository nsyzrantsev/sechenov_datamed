from Bio import Entrez, Medline


def get_xml_list(query_text, articles_number, database_name,):
    Entrez.email = 'some@email.com'
    # Searches and retrieves primary IDs
    handle = Entrez.esearch(
        db=database_name,
        sort='relevance',
        term=query_text,
        pagination='3',
        retmax=articles_number
    )
    id_list = Entrez.read(handle)["IdList"]
    # Retrieve records in the requested format from a list of one or more primary IDs
    articles_handles = Entrez.efetch(db=database_name, id=id_list, rettype="medline", retmode="text")
    articles_xml = Medline.parse(articles_handles)
    # Generation of list of the articles xml
    xml = []
    for article in articles_xml:
        xml.append(article)
    return xml

