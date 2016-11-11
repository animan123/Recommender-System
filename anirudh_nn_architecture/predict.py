from generator import gen

from keras.models import load_model

import numpy as np

import csv

def load_keras_model ():
	return load_model ("char_model_softmax")

def main ():
	model = load_keras_model ()
	data_source = gen ()
	data = data_source.get_validation_data ()
	validation_lists = data_source.validation_data

	output = model.predict (
		[
        	data["user_char"],
           	data["question_tag"],
           	data["user_tags"],
           	data["question_info"],
          	data["question_char"],
		]
	)

	for i in range(len(validation_lists)):
		validation_lists[i].append (float(output[i][1]))
	
	with open("temp.csv", "w") as fp:
		a = csv.writer(fp, delimiter=',')
		a.writerows (validation_lists)
main ()
