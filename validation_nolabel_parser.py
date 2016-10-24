import time
import pandas as pd

def load_validation_data(df, col_name, col_val):
	df = df.set_index([col_name])
	data = df.loc[df.index.isin(col_val)]
	return data

def load_all_validation_data(size=1.0):
	t_start = time.time()
	data =  pd.read_csv("raw_data/validate_nolabel.txt", names = ['q_id','u_id', 'label'], sep = ",")
	print "Returning" +  str(size*100) + "% of data"
	data = data.sample(frac = size)
	t_end = time.time()
	print "Time to load data: ", (t_end - t_start)
	return data

