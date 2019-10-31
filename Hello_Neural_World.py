# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix

# Importing the dataset
dataset = pd.read_csv('C:\\Users\Sergi\Desktop\Artificial_Neural_Networks\Churn_Modelling.csv')
# Выбор всех строк в соответствующих столбцах
X = dataset.iloc[:, 3:13].values
y = dataset.iloc[:, 13].values

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
# LabelEncoder преобразует существующие значения в значения от 0 до n класса значений
labelencoder_X_1 = LabelEncoder()
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])
labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])
# Создание дамми-переменных из категориальной страновой переменной. Затем одна 
# дамми-переменная удаляется, тк нужна линейная независимость
onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()
X = X[:, 1:]

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting classifier to the Training set
# Create your classifier here
from keras.models import Sequential # initializes neural network
from keras.layers import Dense # creates the layers

classifier = Sequential()
# создание входного слоя и одного скрытого, определение стартовых весов и активационной функции (rectifier)
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu', input_dim=11))
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))
classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))

classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
classifier.fit(X_train, y_train, batch_size=10, nb_epoch=100)
# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)
# Making the Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

# k-fold cross-validation (используется для оценки модели и её реальной точности для того, чтобы избежать ситуации
# переобучения, когда модель показывает на обучающей выборке лучшие результаты по сравнению с тествовой. Подбираются
# k выборок, который тестируются на k-1 выборке.

from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score

def build_classifier():
	classifier = Sequential()
	classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu', input_dim=11))
	classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))
	classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))
	classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	return classifier
classifier = KerasClassifier(build_fn = build_classifier, batch_size=10, nb_epoch=100)
accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10, n_jobs = -1)
# n_jobs определеяет, какое количество ресурсов CPU можно занять обучением (-1 - все доступные ресурсы)
mean = accuracies.mean()
variance = accuracies.std()

# Dropout regularisation (is needed to reduce overfitting of the model)
# Часть нейронов за прогон случайно дезактивируется. Таким образом, нейроны
# обучаются более независимо друг от друга, что предохраняет от переобучения.

from keras.layers import Dropout

classifier = Sequential()
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu', input_dim=11))
classifier.add(Dropout(p = 0.1))
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))
classifier.add(Dropout(p = 0.1))
classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))
classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
classifier.fit(X_train, y_train, batch_size=10, nb_epoch=100)


# Tuning the ANN

from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV	# Может быть ошибка

def build_classifier(optimizer):
	classifier = Sequential()
	classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu', input_dim=11))
	classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))
	classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))
	classifier.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
	return classifier
classifier = KerasClassifier(build_fn = build_classifier)
# Начинается с создания словаря для переменных, которые подлежат оптимизации
parameters = {
'batch_size': [25, 32],
'nb_epoch': [100, 500],
'optimizer': ['adam', 'rmsprop']
}
grid_search = GridSearchCV(estimator = classifier, param_grid = parameters, scoring = 'accuracy', cv = 10)
grid_search = grid_search.fit(X_train, y_train)
best_parameters = grid_search.best_params_
best_accuracy = grid_search.best_score_
