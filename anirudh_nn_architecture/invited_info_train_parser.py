import time
import pandas as pd
from sklearn.model_selection import train_test_split

def load_invited_info_data (size=1.0):
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
		return data
	else:
		print "Returning ", size, "times invited info data"
		data = data.sample(frac=size)

def load_invited_info_split (test_size=0.2):
	data = load_invited_info_data()
	return train_test_split(data, test_size = test_size)


