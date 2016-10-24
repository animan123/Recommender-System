from question_info_parser import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy.random import normal


def histogram_question_tag():
	matplotlib.use('Agg')
	df = load_all_question_info_data()
	x = np.array(df.loc[:]["q_tags"])
	plt.hist(x)
	plt.title("question tag histogram")
	plt.xlabel("tag bucket")
	plt.ylabel('bucket count')
	fig1 = plt.gcf()
	fig1.savefig("plots/question_tags_histogram")



#histogram_question_tag()
