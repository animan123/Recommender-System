import operator
import pylab as pl
from sklearn.svm import SVC
import numpy as np
import random
import matplotlib.pyplot as plt
from validation_nolabel_parser import *
import json

np.set_printoptions(threshold=np.nan)

total_q_tags = 20

X1 = np.load("positiveData")
X0 = np.load("negativeData")
UTG1 = np.load("positiveUTG")
UTG0 = np.load("negativeUTG")
validation_set = np.load("validationData")
#question_words_count = json.load("question_words_count")


X_train = []
X_test = []
y_train = []
y_test = []
predict = []
best_e_tags_in_positive = []
best_e_tags_in_negative = []
best_e_tags_in_validation = []
clf_vector = []

question_words_count = {}

with open('question_words_count') as data_file:
        question_words_count = json.load(data_file)

plt.bar(np.arange(len(question_words_count)), question_words_count.values())
plt.xticks(np.arange(len(question_words_count)), question_words_count.keys())
ymax = max(question_words_count.values()) + 1
plt.ylim(0, ymax)
fig1 = plt.gcf()
fig1.savefig("question_word_count")
plt.clf()

sorted_question_words_count = sorted(question_words_count.items(), key=operator.itemgetter(1))
sorted_question_words_count = [int(i[1]) for i in sorted_question_words_count]

plt.bar(np.arange(len(sorted_question_words_count)), sorted_question_words_count)
plt.xticks(np.arange(len(sorted_question_words_count)))
ymax = max(sorted_question_words_count) + 1
plt.ylim(0, ymax)
fig1 = plt.gcf()
fig1.savefig("sorted_question_word_count")
plt.clf()
"""
for i in range(0,total_q_tags):
	yo = np.divide(np.sum(X1[i],axis = 0),X1[i].shape[0])
	best_e_tags_in_positive.append(np.argmax(yo))
	plt.plot(yo)
	yo = np.divide(np.sum(X0[i],axis = 0),X0[i].shape[0])
        best_e_tags_in_negative.append(np.argmax(yo))
        plt.plot(yo)
	yo = np.divide(np.sum(validation_set[i],axis = 0),validation_set[i].shape[0])
        best_e_tags_in_validation.append(np.argmax(yo))
        plt.plot(yo)
	fig1 = plt.gcf()
        fig1.savefig("plots/"+str(i))
	plt.clf()

"""

"""
negative_grp_count_best_tag = []
for i in range(0,total_q_tags):
	x = X0[i]
	negative_grp_count_best_tag.append(np.array(x.shape[0] - np.sum(x[:,best_e_tags_in_positive[i]]))/x.shape[0])
plt.plot(negative_grp_count_best_tag,'b',label = 'ans = 0 when best tag not present')
fig1 = plt.gcf()
fig1.savefig("plots/negative_grp")
plt.clf()


for i in range(0,total_q_tags):
	plt.hist(UTG1[i][0:200,0],50,range = [0,5000],label = '+ve',normed=True)
	plt.hist(UTG0[i][0:200,0],50,range = [0,5000],label = '-ve',normed=True)
	fig1 = plt.gcf()
	fig1.savefig("upvotes/positive_examples/"+str(i))
	plt.clf()

	plt.hist(UTG1[i][0:200,1],50,range = [0,5000],label = '+ve',normed=True)
	plt.hist(UTG0[i][0:200,1],50,range = [0,5000],label = '-ve',normed=True)
	fig1 = plt.gcf()
	fig1.savefig("total_answers/positive_examples/"+str(i))
	plt.clf()

	plt.hist(UTG1[i][0:200,2],50,range = [0,5000],label = '+ve',normed=True)
	plt.hist(UTG0[i][0:200,2],50,range = [0,5000],label = '-ve',normed=True)
	fig1 = plt.gcf()
	fig1.savefig("good_answers/positive_examples/"+str(i))
	plt.clf()

"""
