from generator import gen

from keras.layers import merge, Input, Dense, Dropout
from keras.models import Model
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.optimizers import Adam

import numpy as np

def get_model ():
	question_words = Input(shape=(4022, ), name='Question words')
	user_words = Input(shape=(4022, ), name='User words')
	word_compresser = Dense (70, activation='relu')
	question_word_output = word_compresser (question_words)
	user_word_output = word_compresser (user_words)
	word_merged = merge ([question_word_output, user_word_output], mode='concat')
	word_merged = Dropout (0.45) (word_merged)
	word_merged = Dense (20, activation='relu') (word_merged)
	word_merged = Dropout (0.3) (word_merged)
	word_merged = Dense (10, activation='relu') (word_merged)
	word_merged = Dropout(0.2, name='word merged dropout') (word_merged)
	word_similarity = Dense (5, activation='relu', name='word similarity') (word_merged)

	question_tag = Input(shape=(20, ), name='Question tag')
	user_tags = Input(shape=(143, ), name='User tag')
	user_tags_compressed = Dense (15, activation='relu') (user_tags)
	question_tag_compressed = Dense (15, activation='relu') (question_tag)
	tag_merged = merge([question_tag, user_tags_compressed], mode='concat', name='tag merged')
	tag_similarity = Dense (10, activation='relu') (tag_merged)
	tag_similarity = Dense (5, activation='relu', name='Tag similarity') (tag_similarity)

	question_info = Input(shape=(3, ), name='Question info')
	question_popularity = Dense (4, activation='relu') (question_info)
	question_popularity = Dense (5, activation='relu') (question_popularity)
	question_popularity = Dense (3, activation='relu') (question_popularity)
	question_popularity = Dense (1, activation='sigmoid', name='question_popularity') (question_popularity)

	all_features = merge ([word_similarity, tag_similarity, question_popularity], mode='concat')
	final_output = Dense (4, activation='relu') (all_features)
	final_output = Dense (5, activation='relu') (all_features)
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
	adam = Adam (lr=1e-3)
	model.compile (optimizer=adam, loss='categorical_crossentropy' ,metrics=['accuracy'])

	num_epochs = 10
	#model.summary ()
	data_source = gen ()
	data = data_source.all_data ()

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
		nb_epoch=100,
		batch_size=32,
		shuffle=True,
		validation_split=0.2,
		callbacks = [
			ModelCheckpoint (
				"char_model_softmax_5",
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
