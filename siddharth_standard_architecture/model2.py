from sklearn.svm import SVC
import numpy as np
import random
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.nan)

total_q_tags = 20

X1 = np.load("positiveData")
X0 = np.load("negativeData")
UTG1 = np.load("positiveUTG")
UTG0 = np.load("negativeUTG")

X_train = []
X_test = []
y_train = []
y_test = []
predict = []
best_e_tags_in_positive = []
best_e_tags_in_negative = []
clf_vector = []

for i in range(0,total_q_tags):
	z1 = X1[i]
	z0 = X0[i]
	np.random.shuffle(z1)
	np.random.shuffle(z0)
	total_sample_count = min(z1.shape[0],z0.shape[0])
	train_sample_count = 0.7*total_sample_count
	test_sample_count = total_sample_count - train_sample_count
	X_train.append(np.append(z1[0:train_sample_count,:],z0[0:train_sample_count,:],axis = 0))
	X_test.append(np.append(z1[train_sample_count:total_sample_count,:],z0[train_sample_count:total_sample_count,:],axis = 0))
	y_train.append(np.append(np.zeros(train_sample_count),np.ones(train_sample_count)))
	y_test.append(np.append(np.zeros(total_sample_count - train_sample_count),np.ones(total_sample_count - train_sample_count)))
	#print X_train[i].shape, y_train[i].shape, X_test[i].shape, y_test[i].shape
	#yo = np.divide(np.sum(z1,axis = 0),z1.shape[0])
	yo = np.sum(z1,axis = 0)
	best_e_tags_in_positive.append(np.argmax(yo))
	#print best_e_tags_in_positive[i]
	#print i,"$$$$$$$$$$$$$", yo
	plt.plot(yo)
	fig1 = plt.gcf()
        fig1.savefig("total_plots/"+str(i))
	plt.clf()

for i in range(0,total_q_tags):
	yo = np.sum(X0[i],axis = 0)
	best_e_tags_in_negative.append(np.argmax(yo))

print np.array(best_e_tags_in_negative) == np.array(best_e_tags_in_positive)

#for i in range(0,total_q_tags):
	#clf = SVC()
	#clf.fit(X_train[i],y_train[i])
	#clf_vector.append(clf)
	#predict.append(clf.predict(X_test[i]))
	#print np.sum(predict[i] == y_test[i])

negative_grp_count_best_tag = []
for i in range(0,total_q_tags):
	x = X0[i]
	negative_grp_count_best_tag.append(np.array(x.shape[0] - np.sum(x[:,best_e_tags_in_positive[i]]))/x.shape[0])
plt.plot(negative_grp_count_best_tag,'b',label = 'ans = 0 when best tag not present')
fig1 = plt.gcf()
fig1.savefig("plots/negative_grp")
plt.clf()


for i in range(0,total_q_tags):
	plt.hist(UTG1[i][:,0],50)
	fig1 = plt.gcf()
	fig1.savefig("upvotes/positive_examples/"+str(i))
	plt.clf()

	plt.hist(UTG1[i][:,1],50)
	fig1 = plt.gcf()
	fig1.savefig("total_answers/positive_examples/"+str(i))
	plt.clf()

	plt.hist(UTG1[i][:,2],50)
	fig1 = plt.gcf()
	fig1.savefig("good_answers/positive_examples/"+str(i))
	plt.clf()

	plt.hist(UTG0[i][:,0],50)
	fig1 = plt.gcf()
	fig1.savefig("upvotes/negative_examples/"+str(i))
	plt.clf()

	plt.hist(UTG0[i][:,1],50)
	fig1 = plt.gcf()
	fig1.savefig("total_answers/negative_examples/"+str(i))
	plt.clf()

	plt.hist(UTG0[i][:,2],50)
	fig1 = plt.gcf()
	fig1.savefig("good_answers/negative_examples/"+str(i))
	plt.clf()
