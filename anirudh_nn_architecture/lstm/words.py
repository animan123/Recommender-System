import generator as gen
from keras.layers import merge, Input, Dense, Dropout, LSTM, Embedding
from keras.optimizers import RMSprop, Adam
from keras.models import Model, load_model
import random
from eval import eval
import numpy as np

import theano
theano.config.openmp = True

def inflate(data):
	new_data = []
	for sample in data:
		if sample[2]:
			for i in range(9):
				new_data.append(sample)
		else:
			new_data.append(sample)
	random.shuffle (new_data)
	return new_data

def get_model ():
	user_words = Input(shape=(47,))
	question_words = Input(shape=(47,))
	encoder = Embedding (input_dim=37811, output_dim=3, input_length=47)
	user_words_encoded = encoder (user_words)
	question_words_encoded = encoder (question_words)
	lstm = LSTM(10)
	user_words_final = lstm (user_words_encoded)
	question_words_final = lstm (question_words_encoded)
	merged_words = merge ([user_words_final, question_words_final], mode='concat')
	words_output = Dense (1, activation='sigmoid') (merged_words)

	user_tags = Input(shape=(143,))
	question_tag = Input(shape=(20,))
	user_tags_mapped = Dense (20, activation='softmax') (user_tags)
	merged_tags = merge ([user_tags_mapped, question_tag], mode='concat')
	tags_output = Dense (1, activation='sigmoid') (merged_tags)

	final_output = merge ([words_output, tags_output], mode='concat')
	final_output = Dense (1, activation='sigmoid') (final_output) 
	
	model = Model (
		input=[
			user_words,
			question_words,
			user_tags,
			question_tag,
		],
		output=final_output
	)
	return model

def to_matrix (map, keys, size):
	mat = np.zeros ((len(keys), size))
	for i in range(len(keys)):
		mat[i][map[keys[i]]] = 1
	return mat

def main ():
	model = get_model ()
	#model.summary ()

	answers = gen.load_answers ()
	random.shuffle (answers)
	val = answers[:49000]
	train = inflate (answers[49000:])

	question_words = gen.load_question_words ()
	user_words = gen.load_user_words ()
	question_tags = gen.load_question_tags ()
	user_tags = gen.load_user_tags ()

	tr_uw = np.matrix([user_words[x[1]] for x in train])
	tr_qw = np.matrix([question_words[x[0]] for x in train])
	tr_ut = to_matrix (user_tags, [x[1] for x in train], 143)
	tr_qt = to_matrix (question_tags, [x[0] for x in train], 20)
	tr_r = np.array([x[2] for x in train])

	val_uw = np.matrix ([user_words[x[1]] for x in val])
	val_qw = np.matrix ([question_words[x[0]] for x in val])
	val_ut = to_matrix (user_tags, [x[1] for x in val], 143)
	val_qt = to_matrix (question_tags, [x[0] for x in val], 20)
	val_r = np.array([x[2] for x in val])
	model.compile (
		optimizer = Adam(),
		loss = 'mse'
	)

	for i in range(15):
		model.fit (
			x = [
				tr_uw,
				tr_qw,
				tr_ut,
				tr_qt,
			],
			y = tr_r,
			nb_epoch = 1,
			shuffle = True,
			validation_data = (
				[
					val_uw,
					val_qw,
					val_ut,
					val_qt,
				],
				val_r
			)
		)

		op = model.predict (
			[
				val_uw,
				val_qw,
				val_ut,
				val_qt,
			]
		)
		my_val = []
		for i in range(len(val)):
			my_val.append ((
				val[i][0], val[i][1], float(op[i])
			))
		print "NDCG: ", eval (val, my_val)

main ()
