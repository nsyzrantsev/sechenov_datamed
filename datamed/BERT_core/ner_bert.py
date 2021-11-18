from bert import Bert


# NER Bert model for finding
# drugs in texts
class NerBert(Bert):
    def __init__(self, device, model, tokenizer, labels_dictionary, batch_size):
        super().__init__(device, model, tokenizer, labels_dictionary, batch_size)

    # The function that splits the dataset on the list of the list
    # if the length of a dataset is more than a batch size
    def split_by_batch_size(self, array):
        return super().split_by_batch_size(array)

    # Predict function for all texts
    def predict_by_bert_ner(self, texts_array):
        batched_array = self.split_by_batch_size(texts_array)
        predictions = []
        for batch in batched_array:
            prediction = self.get_prediction_for_batch(batch)
            predictions.extend(prediction)
        return predictions

    # Predict labels for the one batch
    def get_prediction_for_batch(self, batch):
        tokenizer_dict = self.tokenizer(
            batch,
            return_tensors='pt',
            padding=True,
            truncation=True,
            is_split_into_words=False,
            max_length=512).to(self.device)
        classifier_outputs = self.model(**tokenizer_dict)
        prediction_list = classifier_outputs.logits.tolist()
        result_prediction = []
        for i, label_predictions in enumerate(prediction_list):
            decoded_words = self.get_decoded_words(tokenizer_dict['input_ids'].tolist()[i])
            predicted_labels = self.get_predicted_labels(label_predictions)
            labels = self.tokens_filter(decoded_words, predicted_labels)
            result_prediction.append(labels)
        return result_prediction

    # Checks decoded subword for a token
    # and return boolean
    def is_not_token(self, subword):
        tokens_list = ['[ C L S ]',
                       '# #',
                       '[ S E P ]',
                       '[ P A D ]']
        if subword[0:3] in tokens_list or subword in tokens_list:
            return False
        return True

    # Function that gets the list of tokens
    # and returns the list of decoded words
    def get_decoded_words(self, tokens_list):
        decoded_words = []
        for token in tokens_list:
            decoded_words.append(self.tokenizer.decode(token))
        return decoded_words

    # Gets prediction list from BERT_core model
    # and returns predicted labels by labels dictionary
    def get_predicted_labels(self, label_predictions):
        return super().get_predicted_class(label_predictions)

    # Return lists of words without tokens,
    # such as: [ C L S ], # #, [ S E P ], [ P A D ]
    def tokens_filter(self, decoded_words, predicted_labels):
        labels = []
        for subword, label in zip(decoded_words, predicted_labels):
            if self.is_not_token(subword) is True:
                # Changes name of token to readable
                # Example: B-DRUG -> DRUG
                if label != '-':
                    label = label[2:]
                labels.append(label)
        return labels

    # Import predicted tokens in sentences
    def import_tokens_in_sentences(self, sentences, tokens):
        sentences_with_tokens = []
        for i, sentence in enumerate(sentences):
            new_sentence = []
            for j, word in enumerate(sentence.split()):
                if tokens[i][j] != '-':
                    new_sentence.append(f'[{word}<{tokens[i][j]}>]')
                else:
                    new_sentence.append(word)
            sentences_with_tokens.append(' '.join(new_sentence))
        return sentences_with_tokens
