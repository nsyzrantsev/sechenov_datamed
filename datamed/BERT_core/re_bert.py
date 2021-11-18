from bert import Bert


# BERT_core-RE model for finding
# interactions between drugs
class ReBert(Bert):
    def __init__(self, device, model, tokenizer, labels_dictionary, betch_size):
        super().__init__(device, model, tokenizer, labels_dictionary, betch_size)

    # The function that splits the dataset on the list of the list
    # if the length of a dataset is more than a batch size
    def split_by_batch_size(self, array):
        return super().split_by_batch_size(array)

    def predict_by_bert_re(self, ner_sentences):
        batched_array = self.split_by_batch_size(ner_sentences)
        predictions = []
        for batch in batched_array:
            prediction = self.get_prediction_for_batch(batch)
            predictions.extend(prediction)
        return predictions

    # Return prediction for the batch
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
        result_interactions = self.get_predicted_interactions(prediction_list)
        return result_interactions

    # Return prediction in the words:
    # 'No_interaction' or 'effect' or 'advise' or ...
    # by RElables.json
    def get_predicted_interactions(self, interactions_predicted_list):
        return super().get_predicted_class(interactions_predicted_list)
