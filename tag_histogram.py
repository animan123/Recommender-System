from question_info_parser import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

df = load_all_question_info_data()

#x = df.as_matrix(columns=["q_tags"])
x = np.array(df.loc[:]["q_tags"])
#print x.shape
#hist, bins = np.histogram(x, bins=50)
hist = np.histogram(x,bins = 50)
plt.hist(hist)
plt.title("question tag histogram")
plt.xlabel("tag bucket")
plt.ylabel('bucket count')
plt.figure()
#plot_url = py.plot_mpl(fig, filename='mpl-basic-histogram')
plt.savefig("tags_histogram2")
