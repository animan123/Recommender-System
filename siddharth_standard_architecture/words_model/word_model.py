import numpy as np
import pandas as pd
import json

s = "/"
print s.split('/')

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

"""

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

print user_not_answered_word_counts["418f52ed3a2d2b3814b131e75653ba0f"]


