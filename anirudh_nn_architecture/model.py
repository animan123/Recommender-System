from generator import gen

from keras.layers import merge, Input, Dense
from keras.models import Model
from keras.callbacks import ModelCheckpoint, EarlyStopping

import numpy as np

def get_model ():
	question_words = Input(shape=(4022, ), name='Question words')
	user_words = Input(shape=(4022, ), name='User words')
	word_compresser = Dense (25, activation='relu')
	question_word_output = word_compresser (question_words)
	user_word_output = word_compresser (user_words)
	word_merged = merge ([question_word_output, user_word_output], mode='concat', name='word merged')
	word_similarity = Dense (1, activation='sigmoid', name='word similarity') (word_merged)

	question_tag = Input(shape=(20, ), name='Question tag')
	user_tags = Input(shape=(143, ), name='User tag')
	user_tags_compressed = Dense (20, activation='sigmoid') (user_tags)
	tag_merged = merge([question_tag, user_tags_compressed], mode='concat', name='tag merged')
	tag_similarity = Dense (1, activation='sigmoid', name='tag similairty') (tag_merged)

	question_info = Input(shape=(3, ), name='Question info')
	question_popularity = Dense (10, activation='relu') (question_info)
	question_popularity = Dense (1, activation='sigmoid', name='question_popularity') (question_popularity)

	all_features = merge ([word_similarity, tag_similarity, question_popularity], mode='concat')
	final_output = Dense (10, activation='relu') (all_features)
	final_output = Dense (2, activation='softmax', name='final output') (final_output)

	model = Model (
		input = [
			user_words,
			question_tag,
			user_tags,
			question_info,
			question_words
		],
		output = final_output
	)
	
	return model

def process (Y):
	y = np.zeros ((Y.shape[0], 2))
	for i in range(len(Y)):
		y[i][Y[i]] = 1
	return y

def main ():
	model = get_model ()
	model.compile (optimizer='adam', loss='categorical_crossentropy' ,metrics=['accuracy'])

	num_epochs = 10

	data_source = gen ()
	data = data_source.all_data ()

	for i in range (6):
		print "Attempt: ", i+1
		model.fit (
		[
			data["user_char"],
			data["question_tag"],
			data["user_tags"],
			data["question_info"],
			data["question_char"],
		],
		[
			process (data["output"])
		],
		nb_epoch=5,
		batch_size=32,
		shuffle=True,
		validation_split=0.33,
		callbacks = [
			ModelCheckpoint (
				"char_model_softmax",
				"val_acc",
				save_best_only=True,
			),
			EarlyStopping (
				"val_acc",
				patience=2
			)
		],
	)

main ()
