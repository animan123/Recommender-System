import numpy as np
import scipy.stats as stat
import csv


def load_answered_data ():
	f = open("answered_users_new_features", "r").readlines()
	raw_data = [x.split(' ') for x in f]
	return {
		x[0]: [float(y) for y in x[1:]] for x in raw_data
	} 

def load_unanswered_data ():
	f = open("unanswered_users_new_features", "r").readlines()
	raw_data = [x.split(' ') for x in f]
	return {
		x[0]: [float(y) for y in x[1:]] for x in raw_data
	}	

def load_test_data ():
	f = open("validate_nolabel.txt", "r").readlines()
	return [x.split(',') for x in f]

def main ():
	answered_data = load_answered_data ()
	unanswered_data = load_unanswered_data ()
	test_data = load_test_data ()
	for i in range(5):
		print test_data[i]

main ()
