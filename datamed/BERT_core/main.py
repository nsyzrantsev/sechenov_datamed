import torch
import json
from transformers import BertForTokenClassification, BertForSequenceClassification
from transformers import BertTokenizer
from ner_bert import NerBert
from re_bert import ReBert
from os import path

path_to_BERT = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'BERT_core')


def main(input_sentence):
    batch_size = 10
    sentence = [' '.join(input_sentence.split())]
    initialized_ner = ner_initialization()
    initialized_re = re_initialization()
    NER_model = NerBert(*initialized_ner, batch_size)
    NER_tokens = NER_model.predict_by_bert_ner(sentence)
    NER_sentences = NER_model.import_tokens_in_sentences(sentence, NER_tokens)
    RE_model = ReBert(*initialized_re, batch_size)
    RE_interactions = RE_model.predict_by_bert_re(NER_sentences)
    return result_list(sentence, NER_sentences, RE_interactions)


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
def result_list(sentences, NER_sentences, RE_interactions):
    answer_list = []
    for i, sentence in enumerate(sentences):
        sentence_dict = {
            'text_before_bert': sentence,
            'text_after_bert': NER_sentences[i],
            'ddi': RE_interactions[i]
        }
        answer_list.append(sentence_dict)
    return answer_list
