from question_info_parser import *
from user_info_parser import *

import numpy as np
import random

def load_validation_data ():
	with open("raw_data/validate_nolabel.txt") as f:
		raw_data = [x.split(',') for x in f.readlines ()]
		return [[x[0], x[1].rstrip()] for x in raw_data][1:]

def load_training_data ():
	with open("raw_data/invited_info_train.txt") as f:
		raw_data = [x.split('\t') for x in f.readlines ()]
		raw_data = [[x[0], x[1], int(x[2])] for x in raw_data]
		new_data = []
		for x in raw_data:
			if not x[2]:
				new_data.append(x)
			else:
				for i in range(7):
					new_data.append (x)
		random.shuffle (new_data)
		return new_data

def load_users ():
	df = load_all_user_info_data ()
	return {
		row.e_id: {
			"char": [int(x) for x in row.c_id.split('/') if x],
			"tags": [int(x) for x in row.e_tag.split('/') if x],
		}
		for idx, row in df.iterrows ()
	}

def load_questions ():
	df = load_all_question_info_data ()
	return {
		row.q_id: {
			"char": [int(x) for x in row.char_id_seq.split('/') if x],
			"tag": row.q_tags,
			"upvotes": row.upvote_count,
			"total": row.total_answers,
			"good": row.good_answers
		}
		for idx, row in df.iterrows ()
	}

class gen:
	def __init__ (self, batch_size=5000):
		self.training_data = load_training_data ()
		self.validation_data = load_validation_data ()
		self.questions = load_questions ()
		self.users = load_users ()
		self.batch_size = batch_size
		self.total_samples = len(self.training_data)
		self.start = -self.batch_size

	def trimmed_training_data (self, validate=False):
		if validate:
			return self.validation_data
		return self.training_data [
			self.start:
			min (self.start+self.batch_size, self.total_samples)
		]

	def get_question_info (self, validate=False):
		training_data = self.trimmed_training_data (validate)
		return np.array (
			[
				[
					self.questions[x[0]]["upvotes"],
					self.questions[x[0]]["total"],
					self.questions[x[0]]["good"],
				]
				for x in training_data
			]
		)

	def get_question_words (self, validate=False):
		training_data = self.trimmed_training_data (validate)
		question_words = np.zeros ((len(training_data), 4022))
		for i in range(len(training_data)):
			question_words[i, self.questions[training_data[i][0]]["char"]] += 1
		return question_words

	def get_user_words (self, validate=False):
		training_data = self.trimmed_training_data (validate)
		answer_words = np.zeros ((len(training_data), 4022))
		for i in range(len(training_data)):
			answer_words[i, self.users[training_data[i][1]]["char"]] += 1
		return answer_words

	def get_user_tags (self, validate=False):
		training_data = self.trimmed_training_data (validate)
		answer_tags = np.zeros ((len(training_data), 143))
		for i in range(len(training_data)):
			answer_tags[i, self.users[training_data[i][1]]["tags"]] = 1
		return answer_tags

	def get_question_tag (self, validate=False):
		training_data = self.trimmed_training_data (validate)
		question_tag = np.zeros ((len(training_data), 20))
		for i in range(len(training_data)):
			question_tag[i, self.questions[training_data[i][0]]["tag"]] = 1
		return question_tag

	def get_output (self):
		training_data = self.trimmed_training_data ()
		return np.array ([x[2] for x in training_data])

	def data (self):
		while True:
			self.start += self.batch_size
			if self.start >= self.total_samples:
				break
			yield {
				"question_char": self.get_question_words (),
				"user_char": self.get_user_words (),
				"question_tag": self.get_question_tag (),
				"user_tags": self.get_user_tags (),
				"question_info": self.get_question_info (),
				"output": self.get_output()
			}

	def all_data (self):
		self.batch_size = self.total_samples
		self.start = 0 
		return {
			"question_char": self.get_question_words (),
			"user_char": self.get_user_words (),
			"question_tag": self.get_question_tag (),
			"user_tags": self.get_user_tags (),
			"question_info": self.get_question_info (),
			"output": self.get_output()
		}

	def get_validation_data (self):
		return {
			"question_char": self.get_question_words (True),
			"user_char": self.get_user_words (True),
			"question_tag": self.get_question_tag (True),
			"user_tags": self.get_user_tags (True),
			"question_info": self.get_question_info (True),
		}


