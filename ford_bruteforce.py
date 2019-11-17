import os
import re


def letter_fill(ls, max_len_ls):
    while len(ls) < max_len_ls:
        ls.insert(0, 0)
    return ls


def brute_forces(num_list, rows_dict, letters_list, words_list, n, const):
    results = []
    # Перебор цифр от 0 до 9 для самой первой буквы ил словаря
    for index in num_list:
        # Если текущее n соответствует изначальному, то...
        if n == const:
            print('Поиск значений выполнен на ' + str((index) * 10) + ' процентов')
        # Если n == 0, то рекурсия достигла последнего элемента, и продолжать не нужно
        if n > 0:
            # Букве под номером n из списка уникальных букв letters_list в словаре rows_dict 
            # присваивается цифра index
            rows_dict[letters_list[n]] = index
            # Затем идёт вызов функции для n, меньшего на единицу
            brute_forces(num_list, rows_dict, letters_list, words_list, n - 1, const)
    # Если рекурсия достигает последнего элемента (n не должно быть меньше 0), происходит 
    # проверка текущей комбинации цифр для соответствующих букв
    if n == 0:
        # Список, обозначающий число для каждого из трёх имён
        counter = [0, 0, 0]
        # Цикл, увеличивающий число из counter в соответствии с цифрой буквы и её положением
        for i in range(3):
            # Перебор букв имени
            for power, letter in enumerate(words_list[i]):
                # В зависимости от позиции имени оно умножается на 10 в соответствующей степени
                # В words_list элементы, где вместо букв стоят нули (потому что имена могут быть 
                # разной длины), вызвали бы ошибку при запросе такого ключа в словаре, поэтому 
                # операция сложения оборачивается в конструкцию try except
                try:
                    counter[i] += rows_dict[letter] * 10 ** power
                except:
                    pass
        # В случае равенства результат добавляется в список
        if counter[0] + counter[1] == counter[2]:
            results.append(rows_dict)
            print(counter)
    return results


def par_gen(first_row, second_row, third_row):
    rows_set = set(first_row.lower() + second_row.lower() + third_row.lower())
    # Перечень всех уникальных букв
    letters_list = list(rows_set)
    length = len(letters_list)
    # Словарь из буквы как ключа и цифры
    rows_dict = dict(zip(rows_set, [0 for _ in range(length)]))

    # Три списка из букв имен
    first_row_list = list(first_row.lower())
    second_row_list = list(second_row.lower())
    third_row_list = list(third_row.lower())
    # Максимальная длина имени
    max_row_length = max([len(first_row_list), len(second_row_list), len(third_row_list)])
    # Заполнение начала списков нулями до выравнивания
    first_row_list = letter_fill(first_row_list, max_row_length)
    second_row_list = letter_fill(second_row_list, max_row_length)
    third_row_list = letter_fill(third_row_list, max_row_length)
    # Реверс
    first_row_list.reverse()
    second_row_list.reverse()
    third_row_list.reverse()
    words_list = [first_row_list, second_row_list, third_row_list]

    num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return num_list, rows_dict, letters_list, words_list, length


def make_all(first_row, second_row, third_row):
    num_list, rows_dict, letters_list, words_list, length = par_gen(first_row, second_row, third_row)
    # Передаётся список цифр, словарь букв-ключей и нулей, список уникальных букв, список имен, длина макс слова
    brute_forces(num_list, rows_dict, letters_list, words_list, length - 1, length - 1)


def main():
    os.chdir('/home/alex/Programs/Python')
    file = open('names.txt', 'r', encoding='utf-8')
    # Для получения списка имён
    names = file.read().split('  ')
    for pos, part in enumerate(names):
        names[pos] = part.strip('\n').split(' ')
    print(names)
    # make_all(first_row, second_row, third_row)


if __name__ == '__main__':
    main()
