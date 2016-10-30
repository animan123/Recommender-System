from user_info_parser import *
from question_info_parser import *
from invited_info_train_parser import *

import numpy as np
import csv

def get_dicts ():
	question_df = load_all_question_info_data ()
	upvotes = {}
	total_ans = {}
	good_ans = {}
	for idx, row in question_df.iterrows ():
		upvotes[row.q_id] = int (row.upvote_count)
		total_ans[row.q_id] = int (row.total_answers)
		good_ans[row.q_id] = int (row.good_answers)
		if row.total_answers == 0:
			good_ans[row.q_id] = 0
		else:
			good_ans[row.q_id] = int(row.good_answers) / int(row.total_answers)
	return upvotes, total_ans, good_ans

def load_training_data ():
	return load_invited_info_data ()

def empty_dict ():
	return {
		"upvotes": 0,
		"total_ans": 0,
		"good_ans": 0,
		"answered": 0,
		"unanswered": 0,
		"n": 0,
	}

def main ():
	upvotes, total_ans, good_ans = get_dicts ()
	training_data = load_training_data ()
	
	new_features_answered = {}
	new_features_unanswered = {}

	for idx, row in training_data.iterrows ():
		q_id = row.q_id
		e_id = row.e_id
		answered = int (row.answered)
		if e_id not in new_features_answered:
			new_features_answered[e_id] = empty_dict ()
			new_features_unanswered[e_id] = empty_dict ()
		if answered:
			new_features_answered[e_id]["n"] += 1
			new_features_answered[e_id]["upvotes"] += upvotes[q_id]
			new_features_answered[e_id]["total_ans"] += total_ans[q_id]
			new_features_answered[e_id]["good_ans"] += good_ans[q_id]
		else:
			new_features_unanswered[e_id]["n"] += 1
			new_features_unanswered[e_id]["upvotes"] += upvotes[q_id]
			new_features_unanswered[e_id]["total_ans"] += total_ans[q_id]
			new_features_unanswered[e_id]["good_ans"] += good_ans[q_id]
	
	'''
	answered_list = []
	for e_id in new_features_answered:
		if new_features_answered[e_id]["n"] != 0:
			answered_list.append([
				e_id,
				new_features_answered[e_id]["upvotes"] / new_features_answered[e_id]["n"],
				new_features_answered[e_id]["total_ans"] / new_features_answered[e_id]["n"],
				new_features_answered[e_id]["good_ans"] / new_features_answered[e_id]["n"],
				new_features_answered[e_id]["n"]
			])
	'''

	unanswered_list = []
	for e_id in new_features_unanswered:
		if new_features_unanswered[e_id]["n"] != 0:
			unanswered_list.append([
				e_id,
				new_features_unanswered[e_id]["upvotes"] / new_features_unanswered[e_id]["n"],
				new_features_unanswered[e_id]["total_ans"] / new_features_unanswered[e_id]["n"],
				new_features_unanswered[e_id]["good_ans"] / new_features_unanswered[e_id]["n"],
				new_features_unanswered[e_id]["n"]
			])

	print len(unanswered_list)

	with open("unanswered_users_new_features", "w") as f:
		writer = csv.writer (f, delimiter = ' ')
		writer.writerows (unanswered_list)

main ()
