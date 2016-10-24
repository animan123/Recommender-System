import numpy as np
import pandas as pd
import csv

from invited_info_train_parser import load_invited_info_data
from question_info_parser import load_question_info_data
from validation_nolabel_parser import load_all_validation_data

from sklearn.svm import SVR

def main ():
	index_data = load_invited_info_data()
	question_data = load_question_info_data()

	X = []
	Y = []

	l = open("averaged_answers.txt", "r").readlines()
	l = [x.split() for x in l]
	
	question_dict = {}
	for idx, row in question_data.iterrows():
		question_dict[row.q_id] = (
			int(row.upvote_count),
			int(row.total_answers),
			int(row.good_answers),
		)

	for item in l:
		q_id = item[0]
		score = float(item[1])
		x = [
			question_dict[q_id][0],
			question_dict[q_id][1],
			question_dict[q_id][2],
		]
		X.append(x)
		Y.append(score)

	X = np.array(X)
	Y = np.array(Y ,dtype="|S6")

	print X.shape, Y.shape

	model = SVR(kernel='rbf', C=1e3, gamma=0.1, max_iter=1000).fit(X, Y)

	test_data = load_all_validation_data()

	final_ans = []

	for idx, row in test_data.iterrows():
		q_id = row.q_id
		u_id = row.u_id
		try:
			x = [
			question_dict[q_id][0],
			question_dict[q_id][1],
			question_dict[q_id][2],
			]
		except:
			x = [0, 0, 0]
		x = np.array(x)
		x.reshape(1, -1)
		score = model.predict(x) [0]
		if score < 0:
			score = 0
		f = [q_id, u_id, score]
		final_ans.append(f)
		print f

	with open("temp.csv", "w") as fp:
		a = csv.writer(fp, delimiter=',')
		a.writerows (final_ans)

main()
