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
EVALUATION = [
    ('./data/news/LinksUnknownFake/',   FAKE),
    ('./data/news/LinksUnknownReal/',  REAL)
]
SOURCES = [
    ('./data/news/training_fake/',      FAKE),
    ('./data/news/LinksFakeExtra/',      FAKE),
    ('./data/news/training_real/',    REAL),
    ('./data/news/LinkBBC/',    REAL)
]

# Setup pipeline
pipeline = Pipeline([
    ('vectorizer',  CountVectorizer(ngram_range=(1, 3), stop_words='english', encoding="utf-8")),
    #('tfidf_transformer',  TfidfTransformer()),
    ('classifier',  MultinomialNB()) ])

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

def build_data_frame(path, classification):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text': text, 'class': classification})
        index.append(file_name)
    data_frame = DataFrame(rows, index=index)
    return data_frame


training_data = DataFrame({'text': [], 'class': []})
for path, classification in SOURCES:
    training_data = training_data.append(build_data_frame(path, classification))

training_data = training_data.reindex(numpy.random.permutation(training_data.index))

k_fold = KFold(n_splits=8)
scores = []
total_confusion = numpy.array([[0, 0], [0, 0]])
for training_indices, testing_indices in k_fold.split(training_data):
    training_data_texts = training_data.iloc[training_indices]['text'].values
    training_data_classes = training_data.iloc[training_indices]['class'].values

    pipeline.fit(training_data_texts, training_data_classes)

    testing_data_texts = training_data.iloc[testing_indices]['text'].values
    testing_data_classes = training_data.iloc[testing_indices]['class'].values

    predicted_classes = pipeline.predict(testing_data_texts)

    total_confusion += confusion_matrix(testing_data_classes, predicted_classes)
    score = f1_score(testing_data_classes, predicted_classes, pos_label=FAKE)
    scores.append(score)

print 'Cross-validation results:'
print('Total articles classified:', len(training_data))
print('Score:', sum(scores)/len(scores))
# The average F1 score of the n_split tests
print('Confusion matrix:')
print(total_confusion)

evaluation_data = DataFrame({'text': [], 'class':[]})
for path, classification in EVALUATION:
    evaluation_data = evaluation_data.append(build_data_frame(path, classification))

evaluation_data = evaluation_data.reindex(numpy.random.permutation(evaluation_data.index))

pipeline.fit(training_data['text'].values, training_data['class'].values)
predicted_classes = pipeline.predict(evaluation_data['text'].values)

score = f1_score(evaluation_data['class'].values, predicted_classes, pos_label=FAKE)

print 'Evaluation-set results:'
print('Total articles classified:', len(evaluation_data))
print('Score:', score)
print('Confusion matrix:')
print confusion_matrix(evaluation_data['class'].values, predicted_classes)

print 'Article:     Actual class:     Predicted class:'
for article, actual, predicted in zip(evaluation_data.index.values, evaluation_data['class'].values, predicted_classes):
    newArticle = ""
    i = 0
    for word in article.split(" "):
        if i != 0:
            newArticle = newArticle + word + " "
        i = i + 1
    print newArticle, actual, predicted
