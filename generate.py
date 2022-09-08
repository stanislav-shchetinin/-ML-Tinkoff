import argparse
import pickle
import numpy

#реализация консольного интерфейса
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, help='Путь к файлу, где лежит модель')
parser.add_argument('--prefix', type = str, help='Два слова, с которых начнется генерация (в ковычках "")')
parser.add_argument('--length', type = int, help='Длина генерируемой последовательности')
args = parser.parse_args()

name_model_dir = args.model
prefix_sequence = args.prefix
length_sequence = args.length

#загрузка модели
input = open(name_model_dir, 'rb')
model = pickle.load(input)

print(prefix_sequence, end="")
length_sequence -= 2
current_pair = prefix_sequence.split(" ")
current_pair = tuple(current_pair)

#print(numpy.random.choice(model))

for _ in range(length_sequence):
    if model.get(current_pair) == None:
        print(" а", end="")
        current_pair = (current_pair[1], "а")
    else:
        print( " " + model[current_pair][0], end="" )
        current_pair = (current_pair[1], model[current_pair][0])

