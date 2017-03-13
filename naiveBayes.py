# -*- coding: cp1252 -*-
import os
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

newsTrainer = Trainer(tokenizer)

# You need to train the system passing each text one by one to the trainer module.


#newsSet =[
#    {'text': 'not to eat too much is not enough to lose weight', 'category': 'health'},
#    {'text': 'Russia try to invade Ukraine', 'category': 'politics'},
#    {'text': 'do not neglect exercise', 'category': 'health'},
#    {'text': 'Syria is the main issue, Obama says', 'category': 'politics'},
#    {'text': 'eat to lose weight', 'category': 'health'},
#    {'text': 'you should not eat much', 'category': 'health'}
#]

#testSet.append({'text': 'DETTA KONNER EJ MED', 'category': 'health'})



#news=open(file_path_and_name,"r")
testSet=[]

#training with fake news
path = './data/news/training_fake/'
for filename in os.listdir(path):
    file_path_and_name=path+filename
    news=open(file_path_and_name,"r")
    testSet.append({"text":news,'category': 'fakeNews'})  
    print("de filnamn som hör till fakenews är: " +filename)

#training with real news
path = './data/news/training_real/'    
for filename in os.listdir(path):
    file_path_and_name=path+filename
    news=open(file_path_and_name,"r")
    read=news.read()
    testSet.append({"text":read ,'category': 'realNews'})  
    print("de filnamn som är de riktiga nyheterna är: " +filename)
#for filename in glob.glob(os.path.join(path, '*.txt')):
    # do your stuff

#TESTING
    tmp=[]
for filename in os.listdir(path):
    file_path_and_name=path+filename
    news=open(file_path_and_name,"r")
    tmp.append({"text":"here it will be some sort of test" ,'category': 'realNews'})  
    print("de filnamn som är de riktiga nyheterna är: " +filename)

print(tmp)
#TESTING
#print(testSet)
#print(" den träningsmängd som vi har är: " + str(testSet))

for news in tmp:
    newsTrainer.train(news['text'], news['category'])


# When you have sufficient trained data, you are almost done and can start to use
# a classifier.
newsClassifier = Classifier(newsTrainer.data, tokenizer)

# Now you have a classifier which can give a try to classifiy text of news whose
# category is unknown, yet.
classification = newsClassifier.classify("kommer")

# the classification variable holds the detected categories sorted


print(classification)
