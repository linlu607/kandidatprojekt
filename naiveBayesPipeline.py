import os
import numpy
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline

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

def build_data_frame(path):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text': text})
        index.append(file_name)
    data_frame = DataFrame(rows, index=index)
    return data_frame

def get_best_pipeline(path):
	return joblib.load(path + 'estimatorSettings 0.9032 0.9630.pkl')
	pipeline_score = 0.9032 #0.0
#	for file_name in os.listdir(path):
#		print file_name
#		if float(file_name.split(" ")[1]) > pipeline_score:
#			pipeline = joblib.load(path+file_name)
#			pipeline_score = float(file_name.split(" ")[1])
	print ("Loading a pipeline with an F1 score of %.2f on the evaluation set") % pipeline_score
	return pipeline

pipeline = get_best_pipeline('./data/estimators/pickles/')

data = DataFrame({'text': []})
data = data.append(build_data_frame('./data/news/LinksUnknown/'))
data = data.reindex(numpy.random.permutation(data.index))

predicted_classes = pipeline.predict(data['text'].values)

print "Articles classified: " + str(len(data))
print 'Article:			Predicted class:'
for article, predicted in zip(data.index.values, predicted_classes):
	newArticle = ""
	i = 0
	for word in article.split(" "):
		if i != 0:
			newArticle = newArticle + word + " "
		i = i + 1
    	print newArticle, predicted
