import numpy as np
import scipy.stats as stat
import csv

from question_info_parser import *

upvote_std = 5016.3054571
total_ans_std = 190.604091918
good_ans_std = 0.296286903006

def load_answered_data ():
	f = open("answered_users_new_features", "r").readlines()
	raw_data = [x.split(' ') for x in f]
	return {
		x[0]: [float(y) for y in x[1:]] for x in raw_data
	} 

def load_unanswered_data ():
	f = open("unanswered_users_new_features", "r").readlines()
	raw_data = [x.split(' ') for x in f]
	return {
		x[0]: [float(y) for y in x[1:]] for x in raw_data
	}	

def load_test_data ():
	f = open("validate_nolabel.txt", "r").readlines()
	return [x.split(',') for x in f]

def load_question_dict ():
	df = load_all_question_info_data ()
	return {
		row.q_id: row.q_tags
		for idx, row in df.iterrows ()
	}, {
		row.q_id: row.upvote_count
		for idx, row in df.iterrows ()
	}, {
		row.q_id: row.total_answers
		for idx, row in df.iterrows ()
	}, {
		row.q_id: row.good_answers
		for idx, row in df.iterrows ()
	}

def main ():
	answered_data = load_answered_data ()
	unanswered_data = load_unanswered_data ()
	test_data = load_test_data ()
	tag, upvote, total, good = load_question_dict ()

	printable = []

	for i in range(1, len(test_data)):
		qid = test_data[i][0].rstrip()
		uid = test_data[i][1].rstrip()
		if uid not in answered_data:
			answered_n = 0
		else:
			answered_n = answered_data[uid][0]
			answered_upvote = answered_data[uid][1]
			answered_total_ans = answered_data[uid][3]
			answered_good_ans = answered_data[uid][5]
			answered_tag_list = answered_data[uid][7:]
		if uid not in unanswered_data:
			unanswered_n = 0
		else:
			unanswered_n = unanswered_data[uid][0]
			unanswered_upvote = unanswered_data[uid][1]
			unanswered_total_ans = unanswered_data[uid][3]
			unanswered_good_ans = unanswered_data[uid][5]
			unanswered_tag_list = unanswered_data[uid][7:]

		if not answered_n and not unanswered_n:
			printable.append ([qid, uid, 0])
			continue

		if not answered_n:
			printable.append ([qid, uid, 0])
			continue
		else:
			A = 1
			upvote_pdf = stat.norm (answered_upvote, upvote_std)
			A *= upvote_pdf.pdf (upvote[qid])
			total_ans_pdf = stat.norm (answered_total_ans, total_ans_std)
			A *= total_ans_pdf.pdf (total[qid])
			good_ans_pdf = stat.norm (answered_good_ans, good_ans_std)
			A *= good_ans_pdf.pdf (good[qid])
			A *= answered_tag_list[tag[qid]] / np.sum(answered_tag_list)
			A *= (answered_n) / (answered_n + unanswered_n)

		if not unanswered_n:
			B = 0
		else:
			B = 1
			upvote_pdf = stat.norm (unanswered_upvote, upvote_std)
			B *= upvote_pdf.pdf (upvote[qid])
			total_ans_pdf = stat.norm (unanswered_total_ans, total_ans_std)
			B *= total_ans_pdf.pdf (total[qid])
			good_ans_pdf = stat.norm (unanswered_good_ans, good_ans_std)
			B *= good_ans_pdf.pdf (good[qid])
			B *= unanswered_tag_list[tag[qid]] / np.sum(unanswered_tag_list)
			B *= (unanswered_n) / (answered_n + unanswered_n)

		test_data[i].append ((A) / float(A + B))

		if np.isnan (test_data[i][2]):
			test_data[i][2] = 0

		printable.append ([qid, uid, test_data[i][2]])

	with open("temp.csv", "w") as f:
		a = csv.writer (f, delimiter=',')
		a.writerows (printable)

main ()
