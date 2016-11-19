import numpy as np
from generator import load_answers

def log (x):
	return np.log(x)/np.log(2)

def dcg (rs):
	return rs[0] + np.sum([rs[i] / log(i+1) for i in range(1, len(rs))])

def dcg_k (rs, k):
	return dcg (rs[:k])

def eval_q (ans, k):
	#ans is list of 2 tuple with (real_op, my_op)
	ans = sorted(ans, key=lambda tup:-tup[0])
	sorted_ans = sorted(ans, key=lambda tup:-tup[1])
	ans = [x[0] for x in ans]
	sorted_ans = [x[0] for x in sorted_ans]
	ideal = dcg_k (ans, k)
	if not ideal:
		return 0
	return dcg_k (sorted_ans, k) / float(ideal)

def to_dict (data):
	d = {}
	for q, u, r in data:
		if q not in d:
			d[q] = {}
		d[q][u] = r
	return d

def eval (real_data, my_data):
	real = to_dict (real_data)
	my = to_dict (my_data)
	
	score = 0
	for question in real:
		data = []
		for ans in real[question]:
			data.append ((
				real[question][ans], my[question][ans]
			))
		score += (0.5*eval_q(data, 5) + 0.5*eval_q(data, 10))
	score /= len(real)
	return score
