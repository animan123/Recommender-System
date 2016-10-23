import time
import pandas as pd

def load_user_info_data(df, col_name, col_val):
	df = df.set_index([col_name])
	data = df.loc[df.index.isin(col_val)]
	return data

def load_all_user_info_data(size=1.0):
	t_start = time.time()
	data =  pd.read_csv("raw_data/user_info.txt", names = ['e_id','e_tag','w_id','c_id'], delim_whitespace = True)
	print data.shape
	print "Returning" +  str(size*100) + "% of data"
	data = data.sample(frac = size)
	t_end = time.time()
	print "Time to load data: ", (t_end - t_start)
	return data

data = load_all_user_info_data()
print data.shape

curr_data = load_user_info_data(data, "e_id", ["de5ee6f16417420e8c6825061bbf1a83", "051f10227083374795feec803e1421f5"])
print curr_data['w_id']
