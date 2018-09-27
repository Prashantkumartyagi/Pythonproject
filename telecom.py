import pandas as pd
import numpy as np
import sys
pd.set_option('display.width', 100)
pd.set_option('precision', 2)

df = pd.read_csv("C:/Users/Prashant Tyagi/Desktop/data-analytices/Python/WA_Fn-UseC_-Telco-Customer-Churn.csv").drop("customerID", axis=1)
print(df)
print(df.shape)
print(df.info())
print(df.groupby('Churn').size())

cols =  pd.DataFrame({col_name : sum([int(str(elem).isspace() == True) \
                                 for elem in col]) for col_name, col in df.iteritems()}, index=[0])
cols = cols.rename(index={cols.index[0]: 'blank rows'})
#print(cols)
# See null values before and after converstion of whitespace-only chars to np.nan
#print(df.isnull().values.sum())
df.replace(r'^\s+$', np.nan, regex=True, inplace=True)
#print(df.isnull().values.sum())

df['TotalCharges'] = pd.to_numeric(df.TotalCharges)
#print(df.describe())

null_rows = df[df['TotalCharges'].isnull()]
#print(null_rows[['MonthlyCharges', 'tenure', 'TotalCharges', 'Churn']])

# Look at the shape before and after to be sure they were removed
#print(df.shape)
df = df[df['TotalCharges'].notnull()]
#print(df.shape)

from sklearn.preprocessing import LabelEncoder
df_min =''
df_max =''
le = LabelEncoder()
for col in df:
    if df[col].dtype == 'object':
        if df[col].nunique() == 2:
            df[col] = le.fit_transform(df[col])
        elif df[col].nunique() < 2:
            df[col] = df[col].astype('category').cat.codes
            df_max = df[df['Churn'] == 0]
            df_min = df[df['Churn'] == 1]
from sklearn.utils import resample
df_min_ups = resample(df_min, replace=True, n_samples=5163)
print(df_min.shape)
df_ups = pd.concat([df_min_ups, df_max])
print(df_ups.Churn.value_counts())

X = df_ups.iloc[:, :-1].values
y = df_ups.iloc[:,-1].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

from sklearn import metrics

def print_metrics(y_pred, y_test):
    '''
    Prints accuracy, confusion matrix, and classification report for a given set
    of true and predicted values.
    '''
    print(metrics.accuracy_score(y_test, y_pred))
    print(metrics.confusion_matrix(y_test, y_pred))
    print(metrics.classification_report(y_test, y_pred))

from sklearn.tree import DecisionTreeClassifier, export_graphviz

dt_clf = DecisionTreeClassifier(max_depth=3)
dt_clf.fit(X_train, y_train)
dt_pred = dt_clf.predict(X_test)
print_metrics(dt_pred, y_test)

import pydotplus
import matplotlib.pyplot as plt
import matplotlib.image as img

col_names = df.columns.values.tolist()[:-1]
dot_data = export_graphviz(dt_clf,
                                feature_names=col_names,
                                out_file=None,
                                filled=True,
                                rounded=True)

graph = pydotplus.graphviz.graph_from_dot_data(dot_data)
graph.write_png('telco_tree.png')
plt.figure(figsize=(20,20))
plt.imshow(img.imread(fname='telco_tree.png'))
plt.show()