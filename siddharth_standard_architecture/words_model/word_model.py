import csv
import pickle
import time
import numpy as np
import pandas as pd
import json
from sklearn.model_selection import cross_val_score
from sklearn import linear_model

"""

user_ques_ans_or_not = {}

invited_info_data = pd.read_csv(
			"../../raw_data/invited_info_train.txt",
                	sep="\t",
                	names=[
                        	"q_id",
                        	"e_id",
                        	"answered",
                	]
		)

for i in range(0, invited_info_data.shape[0]):
	print "partA ",float(i)/invited_info_data.shape[0]
	df_row = invited_info_data.iloc[i]
	q_id = str(df_row["q_id"])
	e_id = str(df_row["e_id"])
	answered = int(df_row["answered"])
	if q_id not in user_ques_ans_or_not:
		user_ques_ans_or_not[q_id] = {"answered":{},"not_answered":{}}

	if answered == 0:
		user_ques_ans_or_not[q_id]["not_answered"][e_id] = 1
	elif answered == 1:
		user_ques_ans_or_not[q_id]["answered"][e_id] = 1
		user_ques_ans_or_not[q_id]["not_answered"].pop(e_id,None)

json.dump(user_ques_ans_or_not, open("user_ques_ans_or_not",'w'))

#print user_ques_ans_or_not


ques_word_count = {}

question_info_data = pd.read_csv(
                        "../../raw_data/question_info.txt",
                        sep="\t",
                        names = ["q_id",
                                "q_tags",
                                "word_id_seq",
                                "char_id_seq",
                                "upvote_count",
                                "total_answers",
                                "good_answers"])

for i in range(0, question_info_data.shape[0]):
	#print "partB ",i,float(i)/question_info_data.shape[0]
	df_row = question_info_data.iloc[i]
	q_id = str(df_row["q_id"])
	#print q_id
	word_id_seq = str(df_row["word_id_seq"])
	q_word_array = [0 for i in range(0,13231)]
	split_word_id_seq = word_id_seq.split('/')
	if word_id_seq == "/":
		print "**************************"
		word_list = []
	else:
		word_list = [int(x) for x in split_word_id_seq]
	for val in word_list:
		q_word_array[val] = 1
	ques_word_count[q_id] = q_word_array


json.dump(ques_word_count,open("ques_word_count",'w'))



user_answered_word_counts = {}
user_not_answered_word_counts = {}

with open('ques_word_count') as data_file:
	ques_word_count = json.load(data_file)

with open('user_ques_ans_or_not') as data_file:
        user_ques_ans_or_not = json.load(data_file)

for q_id in user_ques_ans_or_not:
	q_id = str(q_id)
	for e_id in user_ques_ans_or_not[q_id]["answered"]:
		e_id = str(e_id)
		user_words = np.array(ques_word_count[q_id])
		if e_id in user_answered_word_counts:
			user_answered_word_counts[e_id] = user_answered_word_counts[e_id] + user_words
		else:
			user_answered_word_counts[e_id] = user_words

for e_id in user_answered_word_counts:
	user_answered_word_counts[e_id] = user_answered_word_counts[e_id].tolist()

json.dump(user_answered_word_counts,open("user_answered_word_counts",'w'))


for q_id in user_ques_ans_or_not:
        q_id = str(q_id)
        for e_id in user_ques_ans_or_not[q_id]["not_answered"]:
                e_id = str(e_id)
                user_words = np.array(ques_word_count[q_id])
                if e_id in user_not_answered_word_counts:
                        user_not_answered_word_counts[e_id] = user_not_answered_word_counts[e_id] + user_words
                else:
                        user_not_answered_word_counts[e_id] = user_words

for e_id in user_not_answered_word_counts:
        user_not_answered_word_counts[e_id] = user_not_answered_word_counts[e_id].tolist()

json.dump(user_not_answered_word_counts,open("user_not_answered_word_counts",'w'))



with open('user_not_answered_word_counts') as data_file:
        user_not_answered_word_counts = json.load(data_file)

with open('user_answered_word_counts') as data_file:
        user_answered_word_counts = json.load(data_file)


user_word_counts_percent = {}
for e_id in user_not_answered_word_counts:
	e_id = str(e_id)
	na = np.array(user_not_answered_word_counts[e_id])
	if e_id in user_answered_word_counts:
		a = np.array(user_answered_word_counts[e_id])
		percent = a.astype(float)/(na+a)
		percent = np.nan_to_num(percent)
		user_word_counts_percent[e_id] = percent.tolist()
	else:
		percent = 0.0/(na)
		percent = np.nan_to_num(percent)
		user_word_counts_percent[e_id] = percent.tolist()

for e_id in user_answered_word_counts:
	e_id = str(e_id)
	if user_word_counts_percent.get(e_id) == None:
		a = np.array(user_answered_word_counts[e_id])
		percent = a.astype(float)/(a)
		percent = np.nan_to_num(percent)
		user_word_counts_percent[e_id] = percent.tolist()

json.dump(user_word_counts_percent,open("user_word_counts_percent",'w'))



user_features = {}
user_info_data =  pd.read_csv("../../raw_data/user_info.txt", names = ['e_id','e_tag','w_id','c_id'], delim_whitespace = True)
for i in range(0, user_info_data.shape[0]):
        df_row = user_info_data.iloc[i]
	e_tag_array = [0 for i in range(0,143)]
        e_id = str(df_row["e_id"])
        e_tag_seq = str(df_row["e_tag"])
        split_e_tag_seq = e_tag_seq.split('/')
        e_tag_list = [int(x) for x in split_e_tag_seq]
        for val in e_tag_list:
                e_tag_array[val] = 1
	user_features[e_id] = e_tag_array

json.dump(user_features,open("user_features",'w'))

"""
with open('user_features') as data_file:
        user_features = json.load(data_file)


with open('user_ques_ans_or_not') as data_file:
        user_ques_ans_or_not = json.load(data_file)

with open('user_word_counts_percent') as data_file:
	user_word_counts_percent = json.load(data_file)


"""

start_time = time.time()
q_id = "1fb3191c9a2e4333b7939fc488db71d1"
q_X_words = []
q_Y_words = []
q_X_e_tags = []
q_Y_e_tags = []


for e_id in user_ques_ans_or_not[q_id]["answered"]:
        e_id = str(e_id)
        q_X_e_tags.append(user_features[e_id])
        q_Y_e_tags.append(1)

for e_id in user_ques_ans_or_not[q_id]["not_answered"]:
        e_id = str(e_id)
        q_X_e_tags.append(user_features[e_id])
        q_Y_e_tags.append(0)

q_X_e_tags = np.array(q_X_e_tags)
q_Y_e_tags = np.array(q_Y_e_tags)
clf_e_tags = linear_model.LogisticRegression()
#scores = cross_val_score(clf_e_tags, q_X_e_tags, q_Y_e_tags, cv=5)
clf_e_tags.fit(q_X_e_tags, q_Y_e_tags)
z = clf_e_tags.predict_proba(q_X_e_tags)
print q_Y_e_tags
print z[:,1]
#print np.equal(q_Y_e_tags,np.array(z))
#print scores
end_time = time.time()
print "time: ",end_time - start_time


for e_id in user_ques_ans_or_not[q_id]["answered"]:
	e_id = str(e_id)
	q_X_words.append(user_word_counts_percent[e_id])
	q_Y_words.append(1)

for e_id in user_ques_ans_or_not[q_id]["not_answered"]:
        e_id = str(e_id)
        q_X_words.append(user_word_counts_percent[e_id])
        q_Y_words.append(0)

q_X_words = np.array(q_X_words)
q_Y_words = np.array(q_Y_words)
clf_words = linear_model.LogisticRegression()
#scores = cross_val_score(clf_words, q_X_words, q_Y_words, cv=5)
clf_words.fit(q_X_words, q_Y_words)
z = clf_words.predict_proba(q_X_words)
print q_Y_words
print z[:,1]
#print np.equal(q_Y_words,np.array(z))
#print scores
end_time = time.time()
print "time: ",end_time - start_time


"""


"""
clfs_words = {}
clfs_e_tags = {}
count = 0
total_count = len(user_ques_ans_or_not)
for q_id in user_ques_ans_or_not:
	print q_id,count,"out of",total_count
	count = count+1
	q_id = str(q_id)
	q_X_words = []
	q_Y_words = []
	if user_ques_ans_or_not[q_id]["answered"] and user_ques_ans_or_not[q_id]["not_answered"]:
		for e_id in user_ques_ans_or_not[q_id]["answered"]:
		        e_id = str(e_id)
        		q_X_words.append(user_word_counts_percent[e_id])
       			q_Y_words.append(1)
		for e_id in user_ques_ans_or_not[q_id]["not_answered"]:
        		e_id = str(e_id)
        		q_X_words.append(user_word_counts_percent[e_id])
        		q_Y_words.append(0)

		q_X_words = np.array(q_X_words)
		q_Y_words = np.array(q_Y_words)
		clf_words = linear_model.LogisticRegression()
		#scores = cross_val_score(clf_words, q_X_words, q_Y_words, cv=5)
		clf_words.fit(q_X_words, q_Y_words)
		#z = clf_words.predict_proba(q_X_words)
		#print q_Y_words
		#print z[:,1]
		clfs_words[q_id] = clf_words
with open('clfs_words','w') as handle:
	pickle.dump(clfs_words,handle)

"""
with open('clfs_words','r') as handle:
        b = pickle.load(handle)

validation_nolabel_data =  pd.read_csv("../../raw_data/validate_nolabel.txt", names = ['q_id','e_id', 'label'], sep = ",")

final_ans = []
for i in range(1,validation_nolabel_data.shape[0]):
	df = validation_nolabel_data.iloc[i]
	q_id = str(df["q_id"]) 
	e_id = str(df["e_id"])
	z = 0
	if q_id in b:
		clf_words = b[q_id]
		if e_id in user_word_counts_percent:
			x = np.array(user_word_counts_percent[e_id]).reshape(1,-1)
			z = clf_words.predict_proba(x)[0][1]
	f = [q_id,e_id,z]
	final_ans.append(f)

with open("temp.csv", "w") as fp:
	a = csv.writer(fp, delimiter=',')
	a.writerows (final_ans)
