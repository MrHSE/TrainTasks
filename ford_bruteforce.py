import os


def letter_fill(ls, max_len_ls):
    while len(ls) < max_len_ls:
        ls.insert(0, 0)
    return ls


def brute_forces(num_list, rows_dict, letters_list, words_list, n, const):
    results = []
    for index in num_list:
        if n == const:
            print('Поиск значений выполнен на ' + str((index) * 10) + ' процентов')
        if n > 0:
            rows_dict[letters_list[n]] = index
            brute_forces(num_list, rows_dict, letters_list, words_list, n - 1, const)
    if n == 0:
        counter = [0, 0, 0]
        for i in range(3):
            for power, letter in enumerate(words_list[i]):
                try:
                    counter[i] += rows_dict[letter] * 10 ** power
                except:
                    pass
        if counter[0] + counter[1] == counter[2]:
            results.append(rows_dict)
            print(counter)
    return results


def par_gen(first_row, second_row, third_row):
    rows_set = set(first_row.lower() + second_row.lower() + third_row.lower())
    letters_list = list(rows_set)
    length = len(letters_list)
    rows_dict = dict(zip(rows_set, [0 for _ in range(length)]))

    first_row_list = list(first_row.lower())
    second_row_list = list(second_row.lower())
    third_row_list = list(third_row.lower())
    max_row_length = max([len(first_row_list), len(second_row_list), len(third_row_list)])
    first_row_list = letter_fill(first_row_list, max_row_length)
    second_row_list = letter_fill(second_row_list, max_row_length)
    third_row_list = letter_fill(third_row_list, max_row_length)
    first_row_list.reverse()
    second_row_list.reverse()
    third_row_list.reverse()
    words_list = [first_row_list, second_row_list, third_row_list]

    num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return num_list, rows_dict, letters_list, words_list, length


def make_all(first_row, second_row, third_row):
    num_list, rows_dict, letters_list, words_list, length = par_gen(first_row, second_row, third_row)
    brute_forces(num_list, rows_dict, letters_list, words_list, length - 1, length - 1)


def main():
    print(os.getcwd())
    file = open('names.txt', 'r', encoding='utf-8')
    names = file.read().split('  ')
    for pos, part in enumerate(names):
        names.remove(part)
        names.insert(pos, part.split(' '))
    # make_all(first_row, second_row, third_row)


if __name__ == '__main__':
    main()
