from random import randint
from numpy import mean


def sort_neyman(sample):
	k = len(sample) // 2
	if len(sample) == 1:
		return sample[0]
	else:
		s1 = sort_neyman(sample[:k])
		s2 = sort_neyman(sample[k:])
		return s1 + s2


sample = [randint(1, 100) for _ in range(100)]
sum = sort_neyman(sample)
print(sum)
