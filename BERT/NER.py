import torch
import json
from transformers import BertForTokenClassification
from transformers import BertTokenizer

# choosing type of processor unit for the torch: CUDA or CPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# loading pre-trained BERT-NER model from NER5 directory
model = BertForTokenClassification.from_pretrained('NER5')
# loading default pre-trained tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# loading pre-trained model to the device
model.to(device)
# sets model in evaluation (inference) mode
model.eval()

# loading tokens labels from JSON file
with open('labels_dictionary.json') as json_file:
    labels_dictionary = json.load(json_file)


# The function that splits the dataset on the list of the list
# if the length of a dataset is more than a batch size
def split_by_batch_size(array, batch_size):
    if len(array) > batch_size:
        return [array[i:i + batch_size] for i in range(0, len(array), batch_size)]
    return array


# Predict function for all texts
def predict_by_bert_ner(texts_array, max_batch_size=10):
    batched_array = split_by_batch_size(texts_array, max_batch_size)
    predictions = []
    for batch in batched_array:
        prediction = get_prediction_for_batch(batch, model, tokenizer, device)
        print(f'prediction={prediction}')
        predictions.extend(prediction)
    return predictions


# Predict labels for the one batch
def get_prediction_for_batch(batch, model, tokenizer, device):
    tokenizer_dict = tokenizer(
        batch,
        return_tensors='pt',
        padding=True,
        truncation=True,
        is_split_into_words=False,
        max_length=512).to(device)
    classifier_outputs = model(**tokenizer_dict)
    prediction_list = classifier_outputs.logits.tolist()
    result_prediction = []
    for i, label_prediction_list in enumerate(prediction_list):
        decoded_words = get_decoded_words(tokenizer_dict['input_ids'].tolist()[i])
        predicted_labels = get_predicted_labels(label_prediction_list)
        labels = []
        for subword, label in zip(decoded_words, predicted_labels):
            if word_is_token(subword) is False:
                labels.append(label)
        result_prediction.append(labels)
    return result_prediction


# Checks decoded subword for a token
# and return boolean
def word_is_token(subword):
    tokens_list = ['[ C L S ]',
                   '# #',
                   '[ S E P ]',
                   '[ P A D ]']
    if subword[0:3] in tokens_list or subword in tokens_list:
        return False
    return True


# Function that gets the list of tokens
# and returns the list of decoded words
def get_decoded_words(tokens_list):
    decoded_words = []
    for token in tokens_list:
        decoded_words.append(tokenizer.decode(token))
    return decoded_words


# Gets prediction list from BERT model
# and returns predicted labels by labels dictionary
def get_predicted_labels(label_prediction_list):
    predicted_labels = []
    index_of_max_element = label_prediction_list.index(max(label_prediction_list))
    predicted_labels.append(labels_dictionary[str(index_of_max_element)])
    return predicted_labels