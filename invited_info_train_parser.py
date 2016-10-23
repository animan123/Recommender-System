import time
import pandas as pd

def load_invited_info_data(size=1.0):
	t_start = time.time()
	data = pd.read_csv(
		"raw_data/invited_info_train.txt",
		sep="\t",
		names=[
			"q_id",
			"e_id",
			"answered",
		]
	)
	if size == 1.0:
		print "Returning complete invited info data"
	else:
		print "Returning ", size, "times invited info data"
		data = data.sample(frac=size)
	t_end = time.time()
	print "Time to load invited_info_data: ", (t_end - t_start)
	return data

load_invited_info_data(0.1)
