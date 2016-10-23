import numpy as np
import time

def load_invited_info_data(size=1.0):
	t_start = time.time()
	invited_info_data =  open("raw_data/invited_info_train.txt").readlines()
	invited_info_data = [x.split() for x in invited_info_data]
	invited_info_data = [[x[0], x[1], int(x[2])] for x in invited_info_data]
	t_end = time.time()
	print "Time to load data: ", (t_end - t_start)

load_invited_info_data()

