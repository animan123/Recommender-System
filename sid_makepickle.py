from question_info_parser import *
from user_info_parser import *
from invited_info_train_parser import *

total_q_tags = 20
total_e_tags = 143


dict_ques = {}
dict_ques_tag = {}
dict_user = {}

df_ques = load_all_question_info_data()
for i in xrange(0,df_ques.shape[0]):
	q_id = df_ques.loc[i]["q_id"]
	q_tags = df_ques.loc[i]["q_tags"]
	word_id_seq = df_ques.loc[i]["word_id_seq"]
	char_id_seq = df_ques.loc[i]["char_id_seq"]
	upvote_count = df_ques.loc[i]["upvote_count"]
	total_answers = df_ques.loc[i]["total_answers"]
	good_answers = df_ques.loc[i]["good_answers"]




	word_id_seq_np = np.array(word_id_seq.split('/'))
	char_id_seq_np = np.array(char_id_seq.split('/'))
	q_tag_vector = np.zeros(total_q_tags)
	q_tag_vector[q_tags] = 1

	dict_ques[q_id] = np.array([upvote_count,total_answers,good_answers])
	dict_ques_tag[q_id] = q_tag_vector

df_user = load_all_user_info_data()
max_e_tag_value = 0
for i in xrange(0,df_user.shape[0]):
	e_id = df_user.loc[i]["e_id"]
	e_tag = df_user.loc[i]["e_tag"]
	e_tag_np = np.array(e_tag.split('/'),dtype = int)
	e_tag_vector = np.zeros(total_e_tags)
	max_e_tag_value = max(max_e_tag_value,max(e_tag_np))
	e_tag_vector[e_tag_np] = 1
	dict_user[e_id] = e_tag_vector

print "yo",max_e_tag_value

X = []
Y = []
df_invited_info = load_invited_info_data()
for i in range(0,df_invited_info.shape[0]):
	q_id = df_invited_info.loc[i]["q_id"]
	e_id = df_invited_info.loc[i]["e_id"]
	answered = df_invited_info.loc[i]["answered"]
	Y.append(answered)
	q_tag_vector = dict_ques_tag[q_id]
	e_tag_vector = dict_user[e_id]

	q_tag_1_idx = (q_tag_vector == 1)
	q_tag_vector[q_tag_1_idx] = -1

	e_tag_1_idx = (e_tag_vector == 1)
        e_tag_vector[e_tag_1_idx] = -1

	e_tag_0_idx = (e_tag_vector == 0)
        e_tag_vector[e_tag_0_idx] = 1

	q_count_features = dict_ques[q_id]

	complete_feature_vector = np.append(q_count_features,np.multiply(q_tag_vector.reshape(total_q_tags,1), np.transpose(e_tag_vector.reshape(total_e_tags,1))))
	#print complete_feature_vector.shape
	X.append(complete_feature_vector)

X = np.array(X)
Y = np.array(Y)
