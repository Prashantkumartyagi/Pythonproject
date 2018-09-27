# Importing libraries
import pandas as pd
import numpy as np
#import re
#import xgboost as xgb
#import seaborn as sns
#import matplotlib.pyplot as plt

#import plotly.offline as py
#py.init_notebook_mode(connected=True)
#import plotly.graph_objs as go
#import plotly.tools as tls

#from sklearn import tree
#from sklearn.metrics import accuracy_score
#from sklearn.model_selection import KFold
#from sklearn.model_selection import cross_val_score
#from IPython.display import Image as PImage
#from subprocess import check_call
#from PIL import Image, ImageDraw, ImageFont


from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

# split data into training and test data.
train_X, test_X, train_y, test_y = train_test_split(X, y,
                                                    train_size=0.5,
                                                    test_size=0.5,
                                                    random_state=123)
print("Labels for training and testing data")
print(train_y)
print(test_y)



# Read csv file into a pandas dataframe
#df = pd.read_csv("C:/Users/Prashant Tyagi/Desktop/DataSet.csv")

# Take a look at the first few rows
#print(df.head())
#print (df['ID'])
#dataset = pd.read_csv('C:/Users/Prashant Tyagi/Desktop/DataSet.csv', header=None)

#print(dataset.describe())
