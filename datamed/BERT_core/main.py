import torch
import json
from transformers import BertForTokenClassification, BertForSequenceClassification
from transformers import BertTokenizer
from ner_bert import NerBert
from re_bert import ReBert
from os import path
from nltk import tokenize
import re

import nltk
nltk.download('punkt')

path_to_BERT = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'BERT_core')


def main(text):
    batch_size = 10
    # split text into sentences and add whitespace between words and symbols
    sentences = [' '.join(re.findall(r"[A-Za-z@#]+|\S", sentence)) for sentence in tokenize.sent_tokenize(text)]
    initialized_ner = ner_initialization()
    initialized_re = re_initialization()
    ner_model = NerBert(*initialized_ner, batch_size)
    ner_tokens_list = ner_model.predict_by_bert_ner(sentences)
    sentences_after_ner, tokens_count_list = ner_model.import_tokens_into_sentences(sentences, ner_tokens_list)
    re_model = ReBert(*initialized_re, batch_size)
    re_interaction = re_model.predict_by_bert_re(sentences_after_ner)
    return result_list(sentences, sentences_after_ner, tokens_count_list, re_interaction)


# NER-BERT initialization
def ner_initialization():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    path_to_bert_ner = str(path.join(path_to_BERT, 'NER5'))
    model = BertForTokenClassification.from_pretrained(path_to_bert_ner)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    path_to_labels_dict = str(path.join(path_to_BERT, 'labels_dictionary.json'))
    with open(path_to_labels_dict) as json_file:
        labels_dictionary = json.load(json_file)
    model.to(device)
    model.eval()
    return device, model, tokenizer, labels_dictionary


# RE-BERT initialization
def re_initialization():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    path_to_bert_re = str(path.join(path_to_BERT, 'Bert_med_re_v5_cont_ep_3'))
    model = BertForSequenceClassification.from_pretrained(path_to_bert_re)
    path_to_medtokenizer = str(path.join(path_to_BERT, 'MEDtokenizer'))
    tokenizer = BertTokenizer.from_pretrained(path_to_medtokenizer)
    path_to_relabels = str(path.join(path_to_BERT, 'RElabels.json'))
    with open(path_to_relabels) as json_file:
        labels_dictionary = json.load(json_file)
    model.to(device)
    model.eval()
    return device, model, tokenizer, labels_dictionary


# Return result list of texts with predicted labels and interactions
def result_list(sentences_before_ner, sentences_after_ner, tokens_count, re_interactions):
    answer_list = []
    for i, sentence in enumerate(sentences_before_ner):
        if tokens_count[i] > 0:
            sentence_dict = {
                'text_before_bert': sentence,
                'text_after_bert': sentences_after_ner[i],
                'ddi': re_interactions[i],
                'sentence_number': i+1
            }
            answer_list.append(sentence_dict)
    return answer_list

