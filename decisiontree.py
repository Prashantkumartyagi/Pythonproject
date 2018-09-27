import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from sklearn.model_selection import train_test_split

data = pd.read_csv("C:/Users/Prashant Tyagi/Desktop/train.csv")
print(data.info())
print("\n Drone_Type options: ", data["Drone_Type"].value_counts())

data.describe()
data.head()

#setting up new data types
from sklearn.model_selection import train_test_split
dtypes_col= data.columns
dtypes_type_old= data.dtypes
dtypes_type= ['int16', 'bool','category','object','category','float32','int8','int8','object','float32','object','category']
optimized_dtypes = dict(zip(dtypes_col, dtypes_type))

#read data once again with optimized columns
data_optimized = pd.read_csv("C:/Users/Prashant Tyagi/Desktop/train.csv")
test_optimized = pd.read_csv("C:/Users/Prashant Tyagi/Desktop/test.csv")

#splitting data to train and validation
train, valid = train_test_split(data_optimized, test_size=0.2)

combined = {"train":train,
            "valid":valid,
            "test":test_optimized}

print(data_optimized.info())
data_optimized.isnull().sum()
print(data_optimized.isnull().sum())

combined_cleaned = {}
# for i,data in combined.items():
#     combined_cleaned[i] = data.drop('Destination_Region', 1).copy()
#
#     train_numeric = combined_cleaned["train"].select_dtypes(include=['float32', 'int16', 'int8', 'bool'])
#
#     colormap = plt.cm.cubehelix_r
#     plt.figure(figsize=(16, 12))
#
# plt.title('Pearson correlation of numeric features', y=1.05, size=15)
# sns.heatmap(train_numeric.corr(),linewidths=0.1,vmax=1.0, square=True, cmap=colormap, linecolor='white', annot=True)

# category features# category features

# we do not count NaN categories
def Post_Type_percent(categories, column):
    Post_Type_list = []
    for c in categories.dropna():
        count = combined_cleaned["train"][combined_cleaned["train"][column] == c][column].count()
        Post_Type = combined_cleaned["train"][combined_cleaned["train"][column] == c]["Post_Type"].sum() / count
        Post_Type_list.append(Post_Type)
    return Post_Type_list


category_features_list = ["Package_Weight", "Drone_Type", "Origin_Region"]
category_features = {}

# for x in category_features_list:
#     unique_values = combined_cleaned["train"][x].unique()
#     Post_Type = Post_Type_percent(unique_values, x)
#     category_features[x] = [unique_values, Post_Type]
#
#     fig, axs = plt.subplots(1, 3, figsize=(18, 4), sharey=True)
#     cb_dark_blue = (0 / 255, 107 / 255, 164 / 255)
#     cb_orange = (255 / 255, 128 / 255, 14 / 255)
#     cb_grey = (89 / 255, 89 / 255, 89 / 255)
#     color = [cb_dark_blue, cb_orange, cb_grey]
#
#     font_dict = {'fontsize': 20,
#                  'fontweight': 'bold',
#                  'color': "white"}
#
#     for i, cat in enumerate(category_features.keys()):
#         number_categories = len(category_features[cat][0])
#         axs[i].bar(range(number_categories), category_features[cat][1], color=color[:number_categories])
#         axs[i].set_title("Post_Type rate " + cat, fontsize=20, fontweight='bold')
#         for j, indx in enumerate(category_features[cat][1]):
#             label_text = category_features[cat][0][j]
#             x = j
#             y = indx
#             axs[i].annotate(label_text, xy=(x - 0.15, y / 2), **font_dict)
#
#     for i in range(3):
#         axs[i].tick_params(
#             axis='x',  # changes apply to the x-axis
#             which='both',  # both major and minor ticks are affected
#             bottom='off',  # ticks along the bottom edge are off
#             top='off',  # ticks along the top edge are off
#             labelbottom='off')  # labels along the bottom edge are off
#         axs[i].patch.set_visible(False)

# filling NaN in "Drone_Type" and "Origin_Region"

# for i,data in combined_cleaned.items():
#     data["Drone_Type"].fillna(value="S",inplace=True) # S is most popular value
#     mean_Fare = data["Origin_Region"].mean()
#     data["Origin_Region"].fillna(value=mean_Fare,inplace=True)
#
#     # filling NaN in "Age"
#     fig, ax = plt.subplots(figsize=(6, 4))
#     x = combined_cleaned["train"]["Travel_Time"].dropna()
#     hist, bins = np.histogram(x, bins=15)
#
#     # plot of histogram
#     ax.hist(x, normed=True, color='grey')
#     ax.set_title('Travel_Time histogram')
#     plt.show()

# from random import choices
#
#     bin_centers = 0.5 * (bins[:len(bins) - 1] + bins[1:])
#     probabilities = hist / hist.sum()

    # dictionary with random numbers from existing age distribution
    # for i, data in combined_cleaned.items():
    #     data["Travel_Time_rand"] = data["Travel_Time"].apply(lambda v: np.random.choice(bin_centers, p=probabilities))
    #     Age_null_list = data[data["Travel_Time"].isnull()].index
    #
    #     data.loc[Age_null_list, "Travel_Time"] = data.loc[Age_null_list, "Travel_Time_rand"]

from sklearn import preprocessing, tree
from sklearn.model_selection import GridSearchCV

tree_data = {}
tree_data_category = {}
tree_optimized=''
train_columns = ''
for i, data in combined_cleaned.items():
    tree_data[i] = data.select_dtypes(include=['float32', 'int16', 'int8']).copy()
    tree_data_category[i] = data.select_dtypes(include=['category'])

    # categorical variables handling
    for column in tree_data_category[i].columns:
        le = preprocessing.LabelEncoder()
        le.fit(data[column])
        tree_data[i][column + "_encoded"] = le.transform(data[column])

        # finding best fit with gridsearch
        param_grid = {'min_samples_leaf': np.arange(20, 50, 5),
                      'min_samples_split': np.arange(20, 50, 5),
                      'max_depth': np.arange(3, 6),
                      'min_weight_fraction_leaf': np.arange(0, 0.4, 0.1),
                      'criterion': ['gini', 'entropy']}
        clf = tree.DecisionTreeClassifier()
        tree_search = GridSearchCV(clf, param_grid, scoring='average_precision')

        X = tree_data["train"].drop("Id", axis=1)
        Y = combined_cleaned["train"]["Post_Type"]
        tree_search.fit(X, Y)

        # print("Tree best parameters :", tree_search.best_params_)
        # print("Tree best estimator :", tree_search.best_estimator_)
        # print("Tree best score :", tree_search.best_score_)

        tree_best_parameters = tree_search.best_params_
        tree_optimized = tree.DecisionTreeClassifier(**tree_best_parameters)
        tree_optimized.fit(X, Y)

        train_columns = list(tree_data["train"].columns)
        train_columns.remove("Id")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(range(len(X.columns)), tree_optimized.feature_importances_)
        plt.xticks(range(len(X.columns)), X.columns, rotation=90)
        ax.set_title("Feature importance")
        plt.show()

import graphviz

print(tree_optimized)
import sklearn

dot_data=sklearn.tree.export_graphviz(tree_optimized, out_file='tree.dot',
                     feature_names='test',
                     class_names='demo',
                     filled=True, rounded=True,
                     special_characters=True)

dot_data = tree.export_graphviz(tree_optimized,
                                out_file=None,
                                filled=True,
                                rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)
print(graph)


