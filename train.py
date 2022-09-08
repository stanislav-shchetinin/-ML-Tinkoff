import argparse
import os
import re
import pickle

#реализация консольного интерфейса
parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', type=str, help='Директория, в которой лежит коллекция документов')
parser.add_argument('--model', type=str, help='Путь к файлу, в который сохраняется модель')
args = parser.parse_args()

name_input_dir = args.input_dir
name_model_dir = args.model

content_all_texts = ""

#считывание всех файлов из указанной директории
for root, dirs, arr_names_files in os.walk(name_input_dir, topdown=False):
    for name in arr_names_files:
        input = open(name_input_dir + "\\" + name, 'r')
        content = input.read()
        content_all_texts += content
        input.close()

#форматирование текста
content_all_texts = content_all_texts.strip()
content_all_texts = content_all_texts.lower()
arr_words = re.split("[^a-zа-яё]+", content_all_texts)

#создание словаря (слово префикса 1, слово префикса 2, следующее слова) : (кол-во встреч)
dictionary = dict()
for ind in range(len(arr_words) - 2):
    count_dict = dictionary.get((arr_words[ind], arr_words[ind + 1], arr_words[ind + 2]), 0)
    count_dict += 1
    dictionary[ (arr_words[ind], arr_words[ind + 1], arr_words[ind + 2]) ] = count_dict

#создание словаря (слово префикса 1, слово префикса 2) : (следующее слово {встречается макс. раз для пары}, сколько встречается)
model = dict()
for triple in dictionary:
    count_word = dictionary[triple]
    if model.get(triple[:2]) == None:
        model[triple[:2]] = (triple[2], count_word)
    else:
        word, count_mod = model[ triple[:2] ]
        if count_mod < count_word:
            model[triple[:2]] = (triple[2], count_word)

#импорт pickle
output = open(name_model_dir, 'wb')
pickle.dump(model, output)
output.close()
