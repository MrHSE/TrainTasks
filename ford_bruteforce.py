D = 5
a_set = {'D', 'O', 'N', 'A', 'L', 'D', 'G', 'E', 'R', 'A', 'L', 'D', 'R', 'O', 'B', 'E', 'R', 'T'}
don = []
ger = []
rob = []

row = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for G in row:
    print(str(G) + ' цикл перебора')
    for A in row:
        for E in row:
            for R in row:
                for N in row:
                    for O in row:
                        for L in row:
                            for B in row:
                                for T in row:
                                    if (D + D) + 10 * (L + L) + 100 * (A + A) + 1000 * (N + R) + 10000 * (O + E) + 100000 * (D + G) == T + 10 * R + 100 * E + 1000 * B + 10000 * O + 100000 * R:
                                        don.append(str(D) + str(O) + str(N) + str(A) + str(L) + str(D))
                                        ger.append(str(G) + str(E) + str(R) + str(A) + str(L) + str(D))
                                        rob.append(str(R) + str(O) + str(B) + str(E) + str(R) + str(T))

print(str(len(don)) + str(' - длина количества ответов Дональда'))
print(str(len(ger)) + str(' - длина количества ответов Геральда'))
print(str(len(rob)) + str(' - длина количества ответов Роберта'))
don = set(don)
ger = set(ger)
rob = set(rob)
print(str(len(don)) + str(' - длина количества ответов Дональда без повторений'))
print(str(len(ger)) + str(' - длина количества ответов Геральда без повторений'))
print(str(len(rob)) + str(' - длина количества ответов Роберта без повторений'))
