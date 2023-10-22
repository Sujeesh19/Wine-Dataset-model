# -*- coding: utf-8 -*-
"""Wine.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NzOfC-xXcto8mEmOdxB8yUj790Z64L-a

Problem Statement - We have given the chemical analysis of the wine we have to do classification based on the region.
"""

# importing the library dataset
from sklearn.datasets import load_wine

"""Loading the wine dataset and initially the wine dataset is in the form of dictationary"""

wine = load_wine()

"""Printing how feature names and how many features present in the dataset"""

print(wine.feature_names)
print()
print(len(wine.feature_names))

"""Importing the Libraries which are required for the preprocessing, visualising and for making model"""

# importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from scipy.stats import skewnorm, norm
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score, ConfusionMatrixDisplay

"""Converting the dataset into dataframe format because it is present in dictionary format"""

data = pd.DataFrame(wine.data, columns = wine.feature_names)

"""Adding the target column to the dataset, initially target variable is not present"""

data['region'] = wine.target

"""Printing the dataset"""

data

"""Checking the infomation of the dataset, checking null values present or not, and the datatype of each column. All the 14 columns are numerical but initially region column is categorial but it has been label encoded and converted to integer."""

data.info()

"""Describe Method gives the overall statistics of the dataset. If the DataFrame contains numerical data, the description contains these information for each column: count, mean, standard deviation, minimum value, 25 percentile, 50 percentile, 75 percentile and Maximum value."""

data.describe()

"""Checking how many regions are there and the count of each region."""

data['region'].value_counts()

"""Here I am showing the distplot for each column to see whether it is normally distributed or not, and also showing how normal distribution would look like and creating a boxplot to check if outliers are present or not on each column"""

plt.figure(figsize=[20,60])
columns = data.columns
cnt = 1
for col in columns:
    plt.subplot(14, 2, cnt)
    sns.distplot(data[col], fit=norm)
    cnt += 1
    plt.subplot(14, 2, cnt)
    sns.boxplot(data[col])
    cnt += 1
plt.tight_layout()
plt.show()

"""*   Three feature are normally distributed others are skewed
*   6 features contains few outliers (malic_acid, ash, alcalinity_of_ash, magnesium, proanthocyanins, color_intensity)

Handling Outliers
"""

out_col = data.loc[:, ['malic_acid', 'ash', 'alcalinity_of_ash', 'magnesium', 'proanthocyanins', 'color_intensity']]

def outlier_thresholds(data, variable):
    quartile1 = data[variable].quantile(0.25)
    quartile3 = data[variable].quantile(0.75)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


for col in out_col:
    low_limit, up_limit = outlier_thresholds(data, col)
    data.loc[(data[col] < low_limit), col] = data[col].mean()-data[col].std()
    data.loc[(data[col] > up_limit), col] = data[col].mean()+data[col].std()

"""Now checking if outliers are handlded or not"""

plt.figure(figsize=[60, 20])
cnt = 1
for col in out_col:
    plt.subplot(2, 3, cnt)
    sns.boxplot(data[col])
    cnt += 1
plt.tight_layout()
plt.show()

"""Making Correlation to check whether are correlated or not"""

plt.figure(figsize=[10,10])
df = data.corr()
sns.heatmap(df, annot=True)

"""# Splitting the Train test

Selecting the independent feature and dependent feature
"""

X = data.drop(['alcohol', 'malic_acid', 'magnesium', 'color_intensity', 'ash'], axis=1)
y = data.iloc[:, -1].values

"""checking the shape of the dataset"""

X.shape, y.shape

"""y is not in proper shape so doing reshaping it"""

y = y.reshape(y.shape[0], 1)

"""#Standarize the data

Doing the scaling of independent feature so that all feaature comes in same scale or in same range.
"""

X = StandardScaler().fit_transform(X)

"""# Train the classifier

splitting the data into training and testing the splitting is done in the ratio of 80:20 where 80% of the dataset are taken in training while 20% for testing
"""

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 2, test_size=0.2)

"""Randomly taking 5 neighbors and checking for the accuracy"""

knn = KNeighborsClassifier(n_neighbors = 5)

"""Fitting the training dataset to model"""

knn.fit(X_train, y_train)

"""Checking the model score"""

knn.score(X_test, y_test)

"""But this not might the best score there are chances that model score can increase

Checking the accuracy score, precision score, recall score, F1 score for the model
"""

y_pred = knn.predict(X_test)
print("Accuracy Score: %.3f"% accuracy_score(y_test, y_pred,))
print("Precision Score: %.3f"% precision_score(y_test, y_pred, average='micro'))
print("Recall Score: %.3f"% recall_score(y_test, y_pred, average='micro'))
print("F1 Score: %.3f"% f1_score(y_test, y_pred, average='micro'))

cn = confusion_matrix(y_test, y_pred)
cmd = ConfusionMatrixDisplay(confusion_matrix = cn)
cmd.plot()
plt.show()

"""# Performing PCA
Principal compund analysis - It is mainly used for Dimensionality Reduction and also for important feature selection.

When we use PCA - Whenever we need to know our features are independent of each other
"""

X = data.iloc[:, :-1].values
X = StandardScaler().fit_transform(X)

"""intially taking None components"""

components = None

"""creating PCA object by passing None component"""

pca = PCA(n_components=components)

"""while performing pca we have to scale our dataset

Here we are fitting the features in pca model
"""

pca.fit(X)

"""Checking how much variance is explained by each feature"""

print("Variance Explained (in percent) ")
print(pca.explained_variance_ratio_*100)

"""Calculating the cumulative sum of the features"""

print("Cumulative variance (in percent) ")
print(pca.explained_variance_ratio_.cumsum()*100)

components = len(pca.explained_variance_ratio_*100)

"""creating the plot and by analyzing how much feature to be select for pca"""

plt.plot(range(1,components+1), np.cumsum(pca.explained_variance_ratio_*100), marker='o')
plt.xlabel('No. of Components')
plt.ylabel('Explained Variance (in percent)')
plt.show()

"""So selecting how much principal component we need, otherwise it will take all the components"""

pca = PCA(n_components=0.85)
pca.fit(X)
print("Cumulative variance (in percent) ")
print(pca.explained_variance_ratio_.cumsum()*100)
components = len(pca.explained_variance_ratio_.cumsum())

x_pca = pca.transform(X)

# splitting the data into training and testing data
X_train, X_test, y_train, y_test = train_test_split(x_pca, y, test_size = 0.3, shuffle = True, random_state=1)

knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(X_train, y_train)
knn.score(X_test, y_test)

"""# Hyperparameter Tunning  
checking for the best value for k
"""

k_range = range(1,20)
score = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors = k)
    knn.fit(X_train, y_train)
    score.append(knn.score(X_test, y_test))

plt.figure()
plt.xlabel('k Count')
plt.ylabel('Model Accuracy')
plt.plot(k_range, score, marker='o')
plt.grid()
plt.xticks([0, 5, 10, 15, 20, 25])
plt.show()

"""Here we can see that for all values of k the accuracy is same expext for k=2"""

y_pred = knn.predict(X_test)

""" A confusion matrix visualizes and summarizes the performance of a classification algorithm. How much data are correctly labelled"""

cn = confusion_matrix(y_test, y_pred)
cmd = ConfusionMatrixDisplay(confusion_matrix = cn)
cmd.plot()
plt.show()

print("Accuracy Score: %.3f"% accuracy_score(y_test, y_pred,))
print("Precision Score: %.3f"% precision_score(y_test, y_pred, average='micro'))
print("Recall Score: %.3f"% recall_score(y_test, y_pred, average='micro'))
print("F1 Score: %.3f"% f1_score(y_test, y_pred, average='micro'))