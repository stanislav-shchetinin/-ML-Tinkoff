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
dict_trip = dict()
#создание словаря (слово префикса 1, слово префикса 2) : (кол-во встреч)
dict_dbl = dict()
for ind in range(len(arr_words) - 2):
    count_dict_trip = dict_trip.get((arr_words[ind], arr_words[ind + 1], arr_words[ind + 2]), 0)
    count_dict_dbl = dict_dbl.get( (arr_words[ind], arr_words[ind + 1]), 0 )
    count_dict_trip += 1
    count_dict_dbl += 1
    dict_trip[ (arr_words[ind], arr_words[ind + 1], arr_words[ind + 2]) ] = count_dict_trip
    dict_dbl[( arr_words[ind], arr_words[ind + 1] )] = count_dict_dbl

#создание словаря (слово префикса 1, слово префикса 2) : [(следующее слово, вероятность встречи), ...]
model = dict()
for triple in dict_trip:
    count_word = dict_trip[triple]
    count_prefix = dict_dbl[triple[:2]]

    if triple[:2] in model:
        model[triple[:2]].append( ( triple[2], count_word/count_prefix ) )
    else:
        model[triple[:2]] = list()
        model[triple[:2]].append((triple[2], count_word / count_prefix))

# for pr in model:
#     print(pr, end = ": ")
#     print(model[pr])

#импорт pickle
output = open(name_model_dir, 'wb')
pickle.dump(model, output)
output.close()
