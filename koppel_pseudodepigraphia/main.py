
import preprocess_NLP_pkg
import koppel_pseudodepigraphia.config
import koppel_pseudodepigraphia.imposter
import numpy as np
import random,os,re

#english_author_dict = preprocess_NLP_pkg.author_dictionary(koppel_pseudodepigraphia.config.english_corpus_token_path, koppel_pseudodepigraphia.config.english_correct_author_path)
# To create the imposter files. Once files have been created, they can only be loaded
#koppel_pseudodepigraphia.imposter.create_imposters_from_author_dict(english_author_dict, koppel_pseudodepigraphia.config.english_corpus_token_path)


imposter_file_names = koppel_pseudodepigraphia.imposter.load_imposters(koppel_pseudodepigraphia.config.imposters_folder_path)
selected_words = preprocess_NLP_pkg.most_common_words_list(koppel_pseudodepigraphia.config.english_common_words_path, col_num = 1, word_separator ="\t", line_separator ="\n")

#f = imposter_file_names[1]

def create_feature_vector_word_freq(imposter_file_names):
    doc_features_list = []
    author_name_list = []
    for file in imposter_file_names:
        author_name = file.split('_')[0]
        author_name_list.append(author_name)
        text = preprocess_NLP_pkg.read_file(koppel_pseudodepigraphia.config.imposters_folder_path + "/" + file)
        word_freq_dict = preprocess_NLP_pkg.word_freq_count_normalised(text)
        vector = list(preprocess_NLP_pkg.select_word_vector(word_freq_dict, text, selected_words).values())
        doc_features_list.append(vector)
    return (doc_features_list, author_name_list)

def select_X_Y(doc_features_array, author_name_list, same_author = False):
    n = len(author_name_list)-1
    X_index = random.randint(0, n)
    Y_index = random.randint(0, n)
    if same_author is False:
        while(author_name_list[X_index] == author_name_list[Y_index]):
            Y_index = random.randint(0, n)
    else:
        while (author_name_list[X_index] != author_name_list[Y_index]):
            Y_index = random.randint(0, n)
    return (author_name_list[X_index], doc_features_array[X_index], author_name_list[Y_index], doc_features_array[Y_index])

def select_Y_given_X(X_name, doc_features_array, author_name_list, same_author = False):
    n = len(author_name_list) - 1
    Y_index = random.randint(0, n)
    if same_author is False:
        while (X_name == author_name_list[Y_index]):
            Y_index = random.randint(0, n)
    else:
        while (X_name != author_name_list[Y_index]):
            Y_index = random.randint(0, n)
    return (author_name_list[Y_index], doc_features_array[Y_index])


features_tuple = create_feature_vector_word_freq(imposter_file_names)
doc_features_array = np.asarray(features_tuple[0])
author_name_list = features_tuple[1]

for i in range(1,5):
    XY_tuple = select_X_Y(doc_features_array, author_name_list, same_author = True)
    X_author = XY_tuple[0]
    X_fragment = XY_tuple[1]
    Y_author = XY_tuple[2]
    Y_fragment = XY_tuple[3]
    cosine_sim = preprocess_NLP_pkg.cosine_similarity(X_fragment, Y_fragment)
    print(X_author, Y_author, cosine_sim)
