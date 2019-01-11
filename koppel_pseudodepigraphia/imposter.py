'''
This file contains all functions to create imposters
'''

import preprocess_NLP_pkg
import koppel_pseudodepigraphia.config
import re
import os

def create_imposters_from_author_dict(dictionary, token_path):
    for author in dictionary.keys():
        list_of_books = dictionary[author]
        create_imposters(author, list_of_books, token_path)

def create_imposters(author, list_of_books, token_path):
    for book in list_of_books:
        book_text = preprocess_NLP_pkg.read_file(token_path + "/"+ book, 'rb')
        book_sub_texts = split_n_parts(book_text, koppel_pseudodepigraphia.config.imposter_sub_text_size) # sub text list
        n_sub_texts = len(book_sub_texts) # number of sub texts
        for j in range(0,n_sub_texts):
            book_name = re.sub(".txt","",book)
            sub_text_name = author + "_" + book_name + "_" + str(j)+ ".txt"
            print(sub_text_name)
            preprocess_NLP_pkg.write_file(koppel_pseudodepigraphia.config.imposters_folder_path + "/" + sub_text_name, book_sub_texts[j], mode='wb')

def load_imposters(imposters_path):
    files_in_path = os.listdir(imposters_path)
    imposters_docs_names = list(file for file in files_in_path if re.search(".txt", file))
    return imposters_docs_names

def split_n_parts(text, n = 2):
    """
    Splits a given text into a list of sub texts of size n each
    Keyword arguments:
        text -- the text to be split
        n -- size of sub-text
    """
    if n > text.__len__():
        print("Error! Sub text size is greater than text!")
        return
    else:
        text_parts_list = [text[i:i + n] for i in range(0, len(text), n)]
        return text_parts_list[:-1] # removing last element as it might have size less than n

