import time
import pandas as pd
import numpy as np
from _collections import defaultdict
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.pyplot import savefig
from question_info_parser import *
import matplotlib

def plot_user_info_data(df, col_name, k):
	matplotlib.use('Agg')
	countWordTagsDict = defaultdict()
	for index, row in df.iterrows():
		listTags = row[col_name].split("/")
		for val in listTags:
				if val != '':
					val = (int)(val)
					if val not in countWordTagsDict:
						countWordTagsDict[val] = 1
					else:
						countWordTagsDict[val] += 1
	finalDict = defaultdict()
	sorted_x = Counter(countWordTagsDict)
	for k, v in sorted_x.most_common(k):
		finalDict[k] = v
	jet = plt.get_cmap('jet')
	N = len(finalDict)
	plt.bar(range(N), finalDict.values(), align='center', color=jet(np.linspace(0, 1.0, N)))
	plt.xticks(range(N), finalDict.keys(), rotation=25)
	plt.title("User Info Words Frequency")
	plt.xlabel("Word")
	plt.ylabel("Frequency")
	plt.show()
	savefig('user_info_word_plot.png')

def load_all_user_info_data(size=1.0):
	t_start = time.time()
	data =  pd.read_csv("raw_data/user_info.txt", names = ['e_id','e_tag','w_id','c_id'], delim_whitespace = True)
	print "Returning " +  str(size*100) + "% of data"
	data = data.sample(frac = size) 
	t_end = time.time()
	print "Time to load data: ", (t_end - t_start)
	return data

data = load_all_user_info_data()

plot_user_info_data(data, 'w_id', 10)
plot_user_info_data(data, 'c_id', 10)

data = load_all_question_info_data()
plot_user_info_data(data, 'word_id_seq', 10)
plot_user_info_data(data, 'char_id_seq', 10)

