from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

newsTrainer = Trainer(tokenizer)

# You need to train the system passing each text one by one to the trainer module.

testSet=[]
#newsSet =[
#    {'text': 'not to eat too much is not enough to lose weight', 'category': 'health'},
#    {'text': 'Russia try to invade Ukraine', 'category': 'politics'},
#    {'text': 'do not neglect exercise', 'category': 'health'},
#    {'text': 'Syria is the main issue, Obama says', 'category': 'politics'},
#    {'text': 'eat to lose weight', 'category': 'health'},
#    {'text': 'you should not eat much', 'category': 'health'}
#]

testSet.append({'text': 'DETTA KONNER EJ MED', 'category': 'health'})
path = './data/news/'

open(file_path_and_name,"r")

print(testSet)

for news in newsSet:
    newsTrainer.train(news['text'], news['category'])

# When you have sufficient trained data, you are almost done and can start to use
# a classifier.
newsClassifier = Classifier(newsTrainer.data, tokenizer)

# Now you have a classifier which can give a try to classifiy text of news whose
# category is unknown, yet.
classification = newsClassifier.classify("Obama is")

# the classification variable holds the detected categories sorted


print(classification)
