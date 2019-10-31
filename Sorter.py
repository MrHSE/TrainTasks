import math


class Sorter(object):
    """В будущем здесь появится документация класса"""
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

    def bubble_sort(self):         # Пузырьковая сортировка (за одну итерацию всплывает очередное max число)
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
            print(self.var)
            if change_indicator == 0:
                self.status = 'Sorted'
                break

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

    def hairbrush_sort(self):      # Сортировка расчёской (скорее всего, придётся менять)
        f_red = 1.247
        length = len(self.var)
        step = int(length / f_red)
        while step > 1:
            for k in range(int(len(self.var) / step)):
                if self.var[k] > self.var[k + step]:
                    self.var[k], self.var[k + step] = self.var[k + step], self.var[k]
            step = int(step / f_red)
        self.var.bubble_sort(self.var)

    def quick_sort(self):          # Быстрая сортировка (сложность O(nlogn))
        pass


a = [7, 6, 5, 4, 3, 2, 1, 0]
b = Sorter(a)
print(b.silly_sort())
