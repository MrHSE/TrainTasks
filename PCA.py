import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

# PCA аппроксимирует n-размерное облако наблюдений до эллипсоида (тоже n-мерного), полуоси которого 
# будут являться будущими главными компонентами.
# Центр: мат ожидание проекций на оси
# Для описания формы дисперсий мало (используется ковариационная матрица)
# После нормировки она упрощается до xxt
# Дисперсия зависит от порядка величины => может потребоваться нормировка
# После надо найти вектор, который бы максимизировал дисперсию проекции выборки на него

# Направление максимальной дисперсии у проекции всегда совпадает с айгенвектором, 
# имеющим максимальное собственное значение, равное величине этой дисперсии

# Генерация выборки
x = np.arange(1,11).reshape(10, 1)
y = 2 * x + 2*np.random.randn(10).reshape(10, 1)
X = np.hstack((x, y))
X_centered = np.hstack((x - x.mean(), y - y.mean()))
moments = (x.mean(), y.mean())
# Ковариационная матрица
X_cov = np.cov(X_centered, rowvar=False)
# Ковариационная матрица
np.dot(np.transpose(X_centered), X_centered)

# Собственные вектора
l, vecs = np.linalg.eig(X_cov)
v = -vecs[:, 1]
# Матрица проекций
Xnew = np.dot(np.transpose(v), np.transpose(X_centered))
print('Новый набор данных', Xnew)
# Значения можно восстановить
n = 9     #номер элемента случайной величины
Xrestored = np.dot(Xnew[n], v) + moments
print('Restored: ' + str(Xrestored))
print('Original: ' + str(X[n, :]))

# Проверка
from sklearn.decomposition import PCA
pca = PCA(n_components = 1)
XPCAreduced = pca.fit_transform(X)
print('Our reduced X: \n', Xnew)
print('Sklearn reduced X: \n', XPCAreduced)
# Сравнение
print('Mean of sk_pca and mine_pca vector: ', pca.mean_, moments)
print('Projection: ', pca.components_, v)
# Отношение собственных значений (дисперсии по осям)
print('Explained variance ratio: ', pca.explained_variance_ratio_, l[1]/sum(l))

# sns.scatterplot(X_centered[0], X_centered[1])
plt.plot(Xnew)
plt.show()
