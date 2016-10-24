import numpy as np
import time
import pandas as pd


def load_question_info_data(df,col_val):
	return df.loc[df["q_id"] == col_val]


def load_all_question_info_data(size=1.0):
	question_info_data = pd.read_csv(
			"raw_data/question_info.txt",
			sep="\t",
			names = ["q_id",
				"q_tags",
				"word_id_seq",
				"char_id_seq",
				"upvote_count",
				"total_answers",
				"good_answers"])

	if size == 1.0:
		print "Returning complete question info data"
		return question_info_data
	else:
		print "Returning", size ,"part of question info data"
		question_info_data = question_info_data.sample(frac = size)
		return question_info_data


def load_all_question_info_data_detail(size=1.0):
        question_info_data = pd.read_csv(
                        "raw_data/question_info.txt",
                        sep="\t",
                        names = ["q_id",
                                "q_tags",
                                "word_id_seq",
                                "char_id_seq",
                                "upvote_count",
                                "total_answers",
                                "good_answers"])
	question_info_data[:]["word_id_seq"] = question_info_data[:]["word_id_seq"].str.split('/')
	question_info_data[:]["char_id_seq"] = question_info_data[:]["char_id_seq"].str.split('/')

        if size == 1.0:
                print "Returning complete question info data"
                return question_info_data
        else:
                print "Returning", size ,"part of question info data"
                question_info_data = question_info_data.sample(frac = size)
                return question_info_data
