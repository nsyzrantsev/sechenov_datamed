import torch
import json
from transformers import BertForTokenClassification, BertForSequenceClassification
from transformers import BertTokenizer
from ner_bert import NerBert
from re_bert import ReBert


def main(texts):
    batch_size = 10
    sentences = [' '.join(string.split()) for string in texts]
    initialized_ner = ner_initialization()
    initialized_re = re_initialization()
    NER_model = NerBert(*initialized_ner, batch_size)
    NER_tokens = NER_model.predict_by_bert_ner(sentences)
    NER_sentences = NER_model.import_tokens(sentences, NER_tokens)
    RE_model = ReBert(*initialized_re, batch_size)
    RE_interactions = RE_model.predict_by_bert_re(NER_sentences)
    return result_list(sentences, NER_sentences, RE_interactions)


# NER-BERT initialization
def ner_initialization():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = BertForTokenClassification.from_pretrained('../datamed/BERT_core/NER5')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    with open('../datamed/BERT_core/labels_dictionary.json') as json_file:
        labels_dictionary = json.load(json_file)
    model.to(device)
    model.eval()
    return device, model, tokenizer, labels_dictionary


# RE-BERT initialization
def re_initialization():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = BertForSequenceClassification.from_pretrained('../datamed/BERT_core/Bert_med_re_v5_cont_ep_3')
    tokenizer = BertTokenizer.from_pretrained('../datamed/BERT_core/MEDtokenizer')
    with open('../datamed/BERT_core/RElabels.json') as json_file:
        labels_dictionary = json.load(json_file)
    model.to(device)
    model.eval()
    return device, model, tokenizer, labels_dictionary


# return result list with predicted labels and interactions
def result_list(sentences, NER_sentences, RE_interactions):
    answer_list = []
    for i, sentence in enumerate(sentences):
        sentence_dict = {
            'Изначальный текст': sentence,
            'После обработки BERT_core': NER_sentences[i],
            'DDI': RE_interactions[i]
        }
        answer_list.append(sentence_dict)
    return answer_list
