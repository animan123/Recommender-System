from question_info_parser import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy.random import normal



matplotlib.use('Agg')

df = load_all_question_info_data()

#x = df.as_matrix(columns=["q_tags"])
x = np.array(df.loc[:]["q_tags"])
#print x.shape
#hist, bins = np.histogram(x, bins=50)
#hist = np.histogram(x,bins = 50)
gaussian_numbers = normal(size=1000)
plt.hist(gaussian_numbers)
plt.title("question tag histogram")
plt.xlabel("tag bucket")
plt.ylabel('bucket count')
plt.figure()
#plot_url = py.plot_mpl(fig, filename='mpl-basic-histogram')
plt.savefig("tags_histogram3")
plt.show()
print gaussian_numbers.shape



