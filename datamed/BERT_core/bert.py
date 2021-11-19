class Bert:
    def __init__(self, device, model, tokenizer, labels_dictionary, batch_size=10):
        self.device = device
        self.model = model
        self.tokenizer = tokenizer
        self.labels_dictionary = labels_dictionary
        self.batch_size = batch_size

    # The function that splits the dataset on the list of the list
    # if the length of a dataset is more than a batch size
    def split_by_batch_size(self, array):
        if len(array) > self.batch_size:
            return [array[i:i + self.batch_size] for i in range(0, len(array), self.batch_size)]
        return array

    # The function that predicts class (interaction or drug) in list
    # from json file
    def get_predicted_class(self, prediction_list):
        text_classes = list(self.labels_dictionary.keys())
        predicted_classes = []
        for word_predictions in prediction_list:
            index_of_max_element = word_predictions.index(max(word_predictions))
            predicted_classes.append(text_classes[index_of_max_element])
        return predicted_classes
