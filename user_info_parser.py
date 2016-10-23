import numpy as np
import time
import pandas as pd

def load_user_info_data(size=1.0):
	t_start = time.time()
	data =  pd.read_csv("raw_data/user_info.txt", names = ['e_id','e_tag','w_id','c_id'], delim_whitespace = True)
	print data.shape 
	if size == 1.0 :
		print "Returning Complete Data"
	else:
		print "Returning" +  str(size*100) + "% of data"
		data = data.sample(frac = size) 
	t_end = time.time()
	print "Time to load data: ", (t_end - t_start)
	return data

data = load_user_info_data(0.2)
print data.shape
