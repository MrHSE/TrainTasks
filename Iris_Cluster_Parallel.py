# Нужно построить scatterplot
# Можно оценить нормальность наблюдений, не отнесённых к кластерам

from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn import metrics
from statsmodels.stats.diagnostic import kstest_normal
from statsmodels.stats.stattools import jarque_bera
import numpy as np
import multiprocessing
from os import getpid
import time
from prettytable import PrettyTable


def fisher_iris():
    print('Импорт ирисов Фишера')
    fishers_iris = load_iris('data')
    data = fishers_iris[0]
    marks = fishers_iris[1]
    return data, marks


def iris_sep(iris, k):
    # Разделение выборки ирисов на части по количеству процессов
    separators = np.arange(0, k + 1)
    iris_final = []
    for sep_num in range(k):
        iris_final.append(iris[int(round(separators[sep_num] * 150 / k, 0)):int(round(separators[sep_num + 1] * 150 / k, 0))])
    return iris_final


def base_matrix(row_num):
    # Генерация нулевой матрицы указанного размера
    print('Генерация нулевой матрицы...')
    return np.zeros((row_num * 10 ** 5, 5))


def population_gen(matrix, iris):
    # заполнение нулевой матрицы ирисами со случайной составляющей
    print('Генерация population на основе Ирисов...')
    for i in range(0, len(matrix) // 10 ** 5):
        print(iris[i, 0])
        for k in range(10 ** 5):
            matrix[10 ** 5 * i + k, 0] += iris[i, 0]
            for j in range(4):
                matrix[10 ** 5 * i + k, j + 1] += iris[i, j + 1] + np.random.normal(0.03, 0.008)
    population = matrix
    return population


def sample_gen(population, ests, procs):
    # генерация подвыборок на данных каждого процесса
    print('Генерация выборок...')
    sample_list = []
    rand_high = len(population)
    for _ in range(ests):
        sam = population[np.random.randint(0, rand_high), :]
        for _ in range(150 // procs):
            sam = np.vstack((sam, population[np.random.randint(0, rand_high)]))
        sample_list.append(sam)
    return sample_list


def get_total_sample_data(procs, ests, total_samples):
    # Сбор подвыборок из каждого процесса в конечную выборку из 15М ирисов
    totat_data = []
    for est in range(ests):
        sample = total_samples[0][est][:, 1:]
        for proc in range(procs - 1):
            sample = np.vstack((sample, total_samples[proc + 1][est][:, 1:]))
        totat_data.append(sample)
    return totat_data


def get_silhouette_list(total_data):
    # Подсчёт коэффициентов силуэта
    silhouette_list = []
    for data in total_data:
        kmeans = KMeans(n_clusters=3).fit(data)
        labels = kmeans.labels_
        silhouette_list.append(metrics.silhouette_score(data, labels, metric='euclidean'))
    return silhouette_list


def data_save(general_pop):
    # Сохранение генеральной совокупности в txt-файл
    output = open('output.txt', 'w')
    output.write('\n'.join(general_pop))


def make_all(data, queue, ests, procs):
    # Функция потоков, выполняет функции, необходимые для генерации
    print('Начало обработки ирисов...')
    zero_matrix = base_matrix(len(data))
    population = population_gen(zero_matrix, data)
    sample_list = sample_gen(population, ests, procs)
    queue.put(sample_list)
    print(queue.qsize())
    print('Завершается работа процесса ' + str(getpid()))


def main():
    procs = int(input("Напишите количество процессов, которые вы хотите использовать для обработки данных: "))
    ests = int(input("Напишите количество выборок, которое вы хотите сгенерировать для проведения кластеризации: "))
    iris, _ = fisher_iris()
    start_time = time.time()
    iris = np.hstack((np.arange(150).reshape((150, 1)), iris))
    iris_samples = iris_sep(iris, procs)
    multiprocessing.set_start_method('fork')
    queue = multiprocessing.Queue()
    processes = []
    for proc in range(procs):
        processes.append(multiprocessing.Process(target=make_all, args=(iris_samples[proc], queue, ests, procs)))
    for process in processes:
        process.start()
    total_samples = []
    for _ in range(procs):
        total_samples.append(queue.get())
    for process in processes:
        process.join()
    # Завершена работа процессов, последующее объединение подвыборок в выборку
    print('Завершение работы процессов')
    total_data = get_total_sample_data(procs, ests, total_samples)
    silhouette_list = get_silhouette_list(total_data)
    print('Список оценённых коэффициентов силуэта')
    sil_time_start = time.time()
    print(silhouette_list)
    print('Время кластеризации и расчёта коэффициентов силуэта для {0} процессов составило: {1}'.format(ests, sil_time_start - time.time()))
    print('Оценка нормальности распределения коэффициентов силуэта')
    print('Тест Харке-Бера')
    print(jarque_bera(silhouette_list))
    PrettyTable
    print('Тест Колмогорова-Смирнова')
    print(kstest_normal(silhouette_list, dist='norm', pvalmethod='approx'))
    # Объединение выборок из каждого потока, расчёт
    print("%s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    main()
