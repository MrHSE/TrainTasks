import os
import re


def letter_fill(ls, max_len_ls):
    while len(ls) < max_len_ls:
        ls.insert(0, 0)
    return ls


def par_gen(first_row, second_row, third_row):
    # Составляем множество всех букв в трёх именах
    letters_set = set(first_row.lower() + second_row.lower() + third_row.lower())
    # Преобразуем множество всех букв в список
    letters_list = list(letters_set)
    # Подсчёт количества букв
    letters_amount = len(letters_list)
    # Создание словаря из всего множества букв и присвоение каждой букве в качестве значения нуля
    letters_dict = dict(zip(letters_set, [0 for _ in range(letters_amount)]))

    # Создание трёх списков из букв каждого из трёх имён
    first_row_list = list(first_row.lower())
    second_row_list = list(second_row.lower())
    third_row_list = list(third_row.lower())
    # Поиск максимально длинного имени
    max_name_length = max([len(first_row_list), len(second_row_list), len(third_row_list)])
    # Пока длина каждого имени не станет равной максимально найденной ранее, на первую позицию добавляются нули
    first_row_list = letter_fill(first_row_list, max_name_length)
    second_row_list = letter_fill(second_row_list, max_name_length)
    third_row_list = letter_fill(third_row_list, max_name_length)
    # Переписывание имён наоборот (теперь нули в конце)
    first_row_list.reverse()
    second_row_list.reverse()
    third_row_list.reverse()
    # Список получившихся имён с нулями
    words_list = [first_row_list, second_row_list, third_row_list]

    # Список цифр
    num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return num_list, letters_dict, letters_list, words_list, letters_amount


def brute_forces(num_list, letters_dict, letters_list, words_list, n, const, name_results_file, triple, results_counter):
    '''
    Схема работы функции
    1) вначале функция получает n и const, равные количеству букв в словах (считая от нуля)
    2) затем в словаре букв букве n (по списку букв letters_list) присваивается цифра index (от нуля до 9)
    3) затем функция вызывает сама себя с n, на единицу меньшим
    
    Таким образом, сначала всем буквам соответствует число 0; в конце, когда достигается конец списка имён,
    и n == 0, то числа, соответствующие буквам имён, складываются (с умножением буквы на 10 в зависимости от позиции буквы в имени)
    Проверяются 9 цифр для последней буквы, затем проверяются 9 цифр для предпоследней буквы и так далее до первой
    
    Пример сложения:    Алиса+
                        Лиза0=
                        Аня00
    Таким образом, складывать можно имена любой длины
    Счётчик counter проверяет сумму получившихся чисел имён
    '''
    for index in num_list:
        
        # const - количество букв
        # Если текущее n соответствует изначальному, то...
        if n == const:
            print('Поиск значений выполнен на ' + str((index) * 10) + ' процентов')
        # Если n == 0, то рекурсия достигла последнего элемента, и продолжать не нужно
        if n > 0:
            # Букве под номером n из списка уникальных букв letters_list в словаре letters_dict 
            # присваивается цифра index
            letters_dict[letters_list[n]] = index
            # Затем идёт вызов функции для n, меньшего на единицу
            brute_forces(num_list, letters_dict, letters_list, words_list, n - 1, const, name_results_file, triple, results_counter)
        # Если рекурсия достигает последнего элемента (n не должно быть меньше 0), происходит 
        # проверка текущей комбинации цифр для соответствующих букв
        
        if n == 0:
            # Букве под номером n из списка уникальных букв letters_list в словаре letters_dict 
            # присваивается цифра index
            letters_dict[letters_list[n]] = index
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
                        counter[i] += letters_dict[letter] * 10 ** power
                    except:
                        pass
            # В случае равенства результат добавляется в список
            if counter[0] + counter[1] == counter[2]:
                # Считаем количество результатов
                results_counter.append('+1')
                print(counter)
                
                # Запись результатов в файл
                first_name_number = ''
                second_name_number = ''
                third_name_number = ''
                names_numbers_list = [first_name_number, second_name_number, third_name_number]
                for name_num, name in enumerate(triple):
                    for letter in name:
                        names_numbers_list[name_num] += str(letters_dict[letter.lower()])
                res_str = triple[0] + ' ({}) + '.format(str(names_numbers_list[0])) + triple[1] + ' ({}) == '.format(str(names_numbers_list[1])) + triple[2] + ' ({})'.format(str(names_numbers_list[2]))
                name_results_file.write(res_str + '\n')
        
        if len(results_counter) > 20:
            return 'Успех'


def make_all(triple, name_results_file):
    print('Поиск чисел для суммы имён: ' + str(triple))
    num_list, letters_dict, letters_list, words_list, letters_amount = par_gen(triple[0], triple[1], triple[2])
    
    results_counter = []
    name_results_file.write(triple[0] + ' + ' + triple[1] + ' = ' + triple[2] + '\n')
    # Передаётся список цифр, словарь букв-ключей и нулей-значений, список уникальных букв, список имен с нулями, длина максимально длинного слова
    brute_forces(num_list, letters_dict, letters_list, words_list, letters_amount - 1, letters_amount - 1, name_results_file, triple, results_counter)
    name_results_file.write('\n')


def main():
    # Загрузка файла со списком имён
    file = open('names.txt', 'r', encoding='utf-8')
    # Тройки имён к сложению в файле разделены двойным пробелом; делим строку имён на тройки
    names = file.read().split('  ')
    # Цикл для итерации в списке троек имён для разделения их на отдельные имена (получается список списков)
    for position in range(len(names)):
        # Замена строки с тройкой имён в списке на список этих имён по отдельности
        names[position] = names[position].strip('\n').split(' ')
    # Так как имена далее будут только считываться, преобразуем список в кортеж
    names = tuple(names)
    # Создание файла, куда ведётся запись удачных результатов
    name_results_file = open('Name_Results.txt', 'w')
    for triple in names:
        make_all(triple, name_results_file)


if __name__ == '__main__':
    main()
