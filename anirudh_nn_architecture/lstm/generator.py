import numpy as np
import csv

def load_questions ():
	with open("questions", "r") as f:
		return [x.rstrip() for x in f.readlines ()]

def load_users ():
	with open("users", "r") as f:
		return [x.rstrip() for x in f.readlines ()]

def load_answers ():
	with open("answers", "r") as f:
		return [
			(
				int(x[0]),
				int(x[1]),
				int(x[2]),
			)
			for x in 
			[y.split(',') for y in f.readlines ()]
		]

def load_inflated_answers ():
	with open("inflated_answers", "r") as f:
		return [
			(
				int(x[0]),
				int(x[1]),
				int(x[2]),
			)
			for x in 
			[y.split(',') for y in f.readlines ()]
		]

def load_question_count ():
	with open("question_count", "r") as f:
		return [
			int(x.rstrip())
			for x in f.readlines ()
		]

def load_user_count ():
	with open("user_count", "r") as f:
		return [
			int(x.rstrip())
			for x in f.readlines ()
		]

def load_question_chars ():
	with open("question_chars", "r") as f:
		return [
			[int(y.rstrip()) for y in x.split(',') if y.rstrip()]
			for x in f.readlines ()
		]

def load_user_chars ():
	with open("user_chars", "r") as f:
		return [
			[int(y.rstrip()) for y in x.split(',') if y.rstrip()]
			for x in f.readlines ()
		]

def load_question_tags ():
	with open("question_tags", "r") as f:
		return [
			int(x.rstrip())
			for x in f.readlines ()
		]

def load_user_tags ():
	with open("user_tags", "r") as f:
		return [
			[int(y.rstrip()) for y in x.split(',') if y.rstrip()]
			for x in f.readlines ()
		]

def load_question_info ():
	with open("question_info.csv", "r") as f:
		return [
			[int(y.strip()) for y in x.split(',')]
			for x in f.readlines ()
		]

def load_user_words ():
	with open("user_words", "r") as f:
		raw = [
			[int(y.rstrip()) for y in x.split(',') if y.rstrip()]
			for x in f.readlines ()
		]
	for x in raw:
		x += [0 for i in range(max(0, 47-len(x)))]
	return raw

def load_question_words ():
	with open("question_words", "r") as f:
		raw = [
			[int(y.rstrip()) for y in x.split(',') if y.rstrip()]
			for x in f.readlines ()
		]
	for x in raw:
		x += [0 for i in range(max(0, 47-len(x)))]
	return raw

