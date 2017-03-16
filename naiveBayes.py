# -*- coding: cp1252 -*-
import os
import numpy
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.pipeline import Pipeline

# Some constant strings
NEWLINE = '\n'
REAL = 'real'
FAKE = 'fake'

def read_files(path):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 200L: # Only files larger than 200 Bytes
            lines = []
            f = open(file_path)
            for line in f:
                lines.append(line)
            f.close()
            content = NEWLINE.join(lines)
            yield file_path, content

##def build_test_frame(path):
##    rows = []
##    index = []
##    for file_name, text in read_files(path):
##        rows.append({'text': text})
##        index.append(file_name)
##
##    test_frame = DataFrame(rows, index=index)
##    return test_frame

def build_data_frame(path, classification):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text': text, 'class': classification})
        index.append(file_name)

    data_frame = DataFrame(rows, index=index)
    return data_frame

pipeline = Pipeline([
    ('vectorizer',  CountVectorizer(ngram_range=(1, 3), stop_words='english', encoding="utf-8")),
    #('tfidf_transformer',  TfidfTransformer()),
    ('classifier',  MultinomialNB()) ])

SOURCES = [
    ('./data/news/training_fake/',      FAKE),
    ('./data/news/training_real/',    REAL)
]

data = DataFrame({'text': [], 'class': []})
for path, classification in SOURCES:
    data = data.append(build_data_frame(path, classification))

data = data.reindex(numpy.random.permutation(data.index))

k_fold = KFold(n_splits=8)
scores = []
total_confusion = numpy.array([[0, 0], [0, 0]])
for training_indices, testing_indices in k_fold.split(data):
    training_data_texts = data.iloc[training_indices]['text'].values
    training_data_classes = data.iloc[training_indices]['class'].values

    pipeline.fit(training_data_texts, training_data_classes)

    testing_data_texts = data.iloc[testing_indices]['text'].values
    testing_data_classes = data.iloc[testing_indices]['class'].values

    predicted_classes = pipeline.predict(testing_data_texts)

    total_confusion += confusion_matrix(testing_data_classes, predicted_classes)
    score = f1_score(testing_data_classes, predicted_classes, pos_label=FAKE)
    scores.append(score)

print('Total articles classified:', len(data))
print('Score:', sum(scores)/len(scores))
# The average F1 score of the n_split tests
print('Confusion matrix:')
print(total_confusion)
