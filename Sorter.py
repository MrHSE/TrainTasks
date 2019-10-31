import math
import time
from random import randint


class Sorter(object):
    """------------------------------Описание------------------------------
    Глупая сортировка: проход ряда, сравнение пар элементов; если старший по
    индексу элемент больше младшего, процесс начинается заново.

    Сортировка пузырьком: сортровка обменами; массив проходится много раз,
    элементы сравниваются попарно; таким образом, после первого прохода
    всплывает первый элемент. Сортировка завершается после прохода без
    обменов.

    Шейкерная сортировка (перемешиванием): вообще ФЗ, как я её сделал.

    Сортировка чёт-нечёт: модификация пузырьковой сортировки; работает
    так же, но отдельно сортируются чётные элементы, отдельно - нечётные.

    Сортировка расчёской: сортировка пузырьком, но с большим шагом; шаг 
    определяется как длина массива, делённая на некий "оптимальный" коэффициент;
    по мере сортировки шаг уменьшается за счёт деления на к-т на каждой итерации;
    когда шаг равен или меньше одного, сортировка завершается пузырьковой.

    Быстрая сортировка: пока не сделал.
    """


    def __init__(self, object):
        self.status = 'Not sorted'
        self.var = object
        # _init_ - метод, который вызывается конструкторов классов Python при
        # создании нового экземпляра класса; соотв-но для создания экземпляра класса
        # требуется передать все необходимые методу _init_ аргументы


    def silly_sort(self):          # Сложность вроде O(n^3)
        length = len(self.var)
        while self.status == 'Not sorted':
            change_indicator = 0
            for k in range(length - 1):
                if self.var[k] > self.var[k + 1]:
                    self.var[k], self.var[k + 1] = self.var[k + 1], self.var[k]
                    change_indicator += 1
                    break
            if change_indicator == 0:
                self.status = 'Sorted'
        return self.var


    def bubble_sort(self):         # Сложность O(n^2)
        length = len(self.var)
        for index, value in enumerate(self.var):
            change_indicator = 0
            for k in range(0, length - index - 1):
                if self.var[k] > self.var[k + 1]:
                    self.var[k], self.var[k + 1] = self.var[k + 1], self.var[k]
                    change_indicator += 1
            if change_indicator == 0:
                self.status = 'Sorted'
                break
        return self.var


    def shaker_sort(self):         # Шейкерная сортировка
        length = len(self.var)
        for index in range(length // 2):
            change_indicator = 0
            for k in range(index, length - index - 1):
                if self.var[k] > self.var[k + 1]:
                    self.var[k], self.var[k + 1] = self.var[k + 1], self.var[k]
                    change_indicator += 1
            for k in range(length - index - 2, index, -1):
                if self.var[k] < self.var[k - 1]:
                    self.var[k], self.var[k - 1] = self.var[k - 1], self.var[k]
                    change_indicator += 1
            if change_indicator == 0:
                self.status = 'Sorted'
                break
        return self.var


    def even_odd(self):            # Чётно-нечётная сортировка
        length = len(self.var)
        if length % 2 == 0:
            c = 0
        else:
            c = 1
        while self.status == 'Not sorted':
            change_indicator = 0
            for k in range(0, length - c, 2):
                if self.var[k] > self.var[k + 1]:
                    self.var[k], self.var[k + 1] = self.var[k + 1], self.var[k]
                    change_indicator += 1
            for k in range(1, length - int(math.cos(c)), 2):
                if self.var[k] > self.var[k + 1]:
                    self.var[k], self.var[k + 1] = self.var[k + 1], self.var[k]
                    change_indicator += 1
            if change_indicator == 0:
                self.status = 'Sorted'
        return self.var


    def hairbrush_sort(self):      # Сортировка расчёской (скорее всего, придётся менять)
        f_red = 1.247
        length = len(self.var)
        step = int(round((length / f_red), 0))
        while step > 1:
            for k in range(int(round(len(self.var) / step, 0))):
                if self.var[k] > self.var[k + step]:
                    self.var[k], self.var[k + step] = self.var[k + step], self.var[k]
            step = int(step / f_red)
        self.bubble_sort()
        return self.var


    def quick_sort(self):          # Быстрая сортировка (сложность O(nlogn))
        pass


print('Генерация данных...')
data = [randint(0, 100) for _ in range(1000)]
sort_it = Sorter(data)
print('Начало работы сортировщиков')
start = time.time()
sil = sort_it.silly_sort()
print('Массив отсортирован за ' + str(time.time() - start) + ' секунд')
start = time.time()
bub = sort_it.bubble_sort()
print('Массив отсортирован за ' + str(time.time() - start) + ' секунд')
start = time.time()
sha = sort_it.shaker_sort()
print('Массив отсортирован за ' + str(time.time() - start) + ' секунд')
start = time.time()
eve = sort_it.even_odd()
print('Массив отсортирован за ' + str(time.time() - start) + ' секунд')
start = time.time()
hai = sort_it.hairbrush_sort()
print('Массив отсортирован за ' + str(time.time() - start) + ' секунд')
'''Итог:
Глупая сортировка: 27.33911
Сортировка пузырьком: 0.00099
Шейкерная сортировка: 0.00100
Сортировка чёт-нечёт: 0.00049
Сортировка расчёской: 0.00150
'''
