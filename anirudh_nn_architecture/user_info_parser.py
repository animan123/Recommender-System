
import time
import pandas as pd

def load_user_info_data(df, col_val):
	return df.loc[df['e_id'] == col_val]

def load_all_user_info_data(size=1.0):
	t_start = time.time()
	data =  pd.read_csv("raw_data/user_info.txt", names = ['e_id','e_tag','w_id','c_id'], delim_whitespace = True)
	data = data.sample(frac = size)
	t_end = time.time()
	return data


