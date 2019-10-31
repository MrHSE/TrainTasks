import math


class Sorter(object):
    """В будущем здесь появится документация класса"""
    def __init__(self):
        self.status = 'Not sorted'
        # _init_ - метод, который вызывается конструкторов классов Python при
        # создании нового экземпляра класса; соотв-но для создания экземпляра класса
        # требуется передать все необходимые методу _init_ аргументы

    def silly_sort(self, row):          # Сложность вроде O(n^3)
        length = len(row)
        while self.status == 'Not sorted':
            change_indicator = 0
            for k in range(length - 1):
                if row[k] > row[k + 1]:
                    row[k], row[k + 1] = row[k + 1], row[k]
                    change_indicator += 1
                    break
                if change_indicator == 0:
                    self.status = 'Sorted'
        return row

    def bubble_sort(self, row):         # Пузырьковая сортировка (за одну итерацию всплывает очередное max число)
        length = len(row)
        for index, value in enumerate(row):
            change_indicator = 0
            for k in range(0, length - index - 1):
                if row[k] > row[k + 1]:
                    row[k], row[k + 1] = row[k + 1], row[k]
                    change_indicator += 1
            if change_indicator == 0:
                self.status = 'Sorted'
                break

    def shaker_sort(self, row):         # Шейкерная сортировка
        length = len(row)
        for index in range(length // 2):
            change_indicator = 0
            for k in range(index, length - index - 1):
                if row[k] > row[k + 1]:
                    row[k], row[k + 1] = row[k + 1], row[k]
                    change_indicator += 1
            for k in range(length - index - 2, index, -1):
                if row[k] < row[k - 1]:
                    row[k], row[k - 1] = row[k - 1], row[k]
                    change_indicator += 1
            print(row)
            if change_indicator == 0:
                self.status = 'Sorted'
                break

    def even_odd(self, row):            # Чётно-нечётная сортировка
        length = len(row)
        if length % 2 == 0:
            c = 0
        else:
            c = 1
        while self.status == 'Not sorted':
            change_indicator = 0
            for k in range(0, length - c, 2):
                if row[k] > row[k + 1]:
                    row[k], row[k + 1] = row[k + 1], row[k]
                    change_indicator += 1
            for k in range(1, length - int(math.cos(c)), 2):
                if row[k] > row[k + 1]:
                    row[k], row[k + 1] = row[k + 1], row[k]
                    change_indicator += 1
            if change_indicator == 0:
                self.status = 'Sorted'

    def hairbrush_sort(self, row):      # Сортировка расчёской (скорее всего, придётся менять)
        f_red = 1.247
        length = len(row)
        step = int(length / f_red)
        while step > 1:
            for k in range(int(len(row) / step)):
                if row[k] > row[k + step]:
                    row[k], row[k + step] = row[k + step], row[k]
            step = int(step / f_red)
        Sort().bubble_sort(row)

    def quick_sort(self, row):          # Быстрая сортировка (сложность O(nlogn))
        pass


a = [7, 6, 5, 4, 3, 2, 1, 0]
Sort().hairbrush_sort(a)
print(a)
