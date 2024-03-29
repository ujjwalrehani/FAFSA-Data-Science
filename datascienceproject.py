# -*- coding: utf-8 -*-
"""DataScienceProject

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Fl807q33rsMgTyLBxQdT8iSKeNlRbL8V

# Data Science Project Notebook
"""

# Data wrangling libraries.
import pandas as pd
import numpy as np

# Other libraries
import math

# Plotting libraries
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette(sns.cubehelix_palette(8, start=2))
from mpl_toolkits import mplot3d
from matplotlib.pyplot import cm

url_income = 'https://raw.githubusercontent.com/urehani1/491/master/Maryland_Median_Household_Income_By_Year_With_Margin_Of_Error__2007-2016.csv'
df_income = pd.read_csv(url_income)
print('File loaded')
display(df_income.head())

df_income=df_income.drop(columns=['Date created'])
df_income = df_income.drop(df_income[df_income.MARYLAND < 1000].index)
df_income.head(15)

#counties = []
counties = list(df_income)
counties = counties[2:]
#print(counties)
color=iter(cm.rainbow(np.linspace(0,1,1)))
c=next(color)
for x in counties:
    x, y = zip(*sorted(zip(df_income['Year'], df_income[x])))
    plt.plot(x,y,label = 'dd')
plt.title('Year vs Median Income for Maryland Counties')
plt.xlabel('Year')
plt.ylabel('Median Income')
#plt.plot(x,y)
plt.show()

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

x = df_income[['Year']]
df_pred_income = pd.DataFrame(columns=['County', 'Income_2017', 'Income_2018', 'Income_2019'])
for i in list(df_income.columns)[2:]:
  #print(type(i))
  y = df_income[[i]]
  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=1)

  regression_model = LinearRegression()
  regression_model.fit(x_train, y_train)
  income = regression_model.predict([[2017]])
  income2 = regression_model.predict([[2018]])
  income3 = regression_model.predict([[2019]])
  #print(i,income[0][0],income2[0][0],income3[0][0])
  df_pred_income = df_pred_income.append({
      'County': i,
      'Income_2017': int(income[0][0]),
      'Income_2018': int(income2[0][0]),
      'Income_2019': int(income3[0][0])
  }, ignore_index=True)
  
# url_newincome = 'https://raw.githubusercontent.com/urehani1/491/master/maryland_income19.csv'
# df_newincome = pd.read_csv(url_newincome)
# df_newincome.head(15)
df_pred_income[['Income_2017', 'Income_2018', 'Income_2019']] = df_pred_income[['Income_2017', 'Income_2018', 'Income_2019']].astype(int)
df_pred_income.head()

df_nces = pd.read_csv('https://media.githubusercontent.com/media/RobRoseKnows/umbc-cs-projects/master/umbc-cs491-data-science/proj/data/csv/ncesdata_md.csv')

df_fafsa = pd.read_csv('https://media.githubusercontent.com/media/RobRoseKnows/umbc-cs-projects/master/umbc-cs491-data-science/proj/data/csv/MD.csv')

df_nces.head()

df_fafsa.head()

# Convert all the school names to uppercase.
df_nces['School Name'] = df_nces['School Name'].apply(lambda x: x.upper())
# Convert Baltimore city to Baltimore City so it will merge properly.
df_nces['County Name*'] = df_nces['County Name*'].replace({'Baltimore city': 'Baltimore City'})
df_nces.head()

df_joined = df_nces.merge(df_fafsa, left_on="School Name", right_on="Name")
df_joined = df_joined.merge(df_pred_income, left_on="County Name*", right_on="County")
df_joined.head()

df_joined.columns.tolist()

# Get rid of any <5 values in Applications by replacing it with 0.
df_joined['Applications_1920_Submitted_Apr19_2019'] = pd.to_numeric(df_joined['Applications_1920_Submitted_Apr19_2019'].astype(str).str.replace(',',''), errors='coerce').fillna(0).astype(int)
df_joined['Applications_1920_Complete_Apr19_2019'] = pd.to_numeric(df_joined['Applications_1920_Complete_Apr19_2019'].astype(str).str.replace(',',''), errors='coerce').fillna(0).astype(int)
df_joined['Applications_1819_Submitted_Apr19_2018'] = pd.to_numeric(df_joined['Applications_1819_Submitted_Apr19_2018'].astype(str).str.replace(',',''), errors='coerce').fillna(0).astype(int)
df_joined['Applications_1819_Complete_Apr19_2018'] = pd.to_numeric(df_joined['Applications_1819_Complete_Apr19_2018'].astype(str).str.replace(',',''), errors='coerce').fillna(0).astype(int)
df_joined['Applications_1819_Submitted_Jun_2018'] = pd.to_numeric(df_joined['Applications_1819_Submitted_Jun_2018'].astype(str).str.replace(',',''), errors='coerce').fillna(0).astype(int)
df_joined['Applications_1819_Complete_Jun_2018'] = pd.to_numeric(df_joined['Applications_1819_Complete_Jun_2018'].astype(str).str.replace(',',''), errors='coerce').fillna(0).astype(int)
df_joined['Applications_1819_Submitted_Dec_2018'] = pd.to_numeric(df_joined['Applications_1819_Submitted_Dec_2018'].astype(str).str.replace(',',''), errors='coerce').fillna(0).astype(int)
df_joined['Applications_1819_Complete_Dec_2018'] = pd.to_numeric(df_joined['Applications_1819_Complete_Dec_2018'].astype(str).str.replace(',',''), errors='coerce').fillna(0).astype(int)

df_joined['Students'] = pd.to_numeric(df_joined['Students*'].astype(str).str.replace(',',''), errors='coerce').fillna(0).astype(int)
df_joined['Teachers'] = pd.to_numeric(df_joined['Teachers*'].astype(str).str.replace(',',''), errors='coerce').fillna(0)
df_joined['Student_Teacher_Ratio'] = pd.to_numeric(df_joined['Student Teacher Ratio*'].astype(str).str.replace(',',''), errors='coerce').fillna(0)

df_joined['Applications_1920_Completed_Submitted_Perc_Apr19_2019'] = df_joined['Applications_1920_Complete_Apr19_2019'] / df_joined['Applications_1920_Submitted_Apr19_2019']
df_joined['Applications_1819_Completed_Submitted_Perc_Apr19_2018'] = df_joined['Applications_1819_Complete_Apr19_2018'] / df_joined['Applications_1819_Submitted_Apr19_2018']
df_joined['Applications_1920_Completed_Submitted_Perc_Apr19_2019'] = df_joined['Applications_1920_Completed_Submitted_Perc_Apr19_2019'].fillna(0)
df_joined['Applications_1819_Completed_Submitted_Perc_Apr19_2018'] = df_joined['Applications_1819_Completed_Submitted_Perc_Apr19_2018'].fillna(0)

df_joined['Applications_1920_Complete_Students_Perc_Apr19_2019'] = df_joined['Applications_1920_Complete_Apr19_2019'] / df_joined['Students']
df_joined['Applications_1819_Complete_Students_Perc_Apr19_2018'] = df_joined['Applications_1819_Complete_Apr19_2018'] / df_joined['Students']
df_joined['Applications_1920_Complete_Students_Perc_Apr19_2019'] = df_joined['Applications_1920_Complete_Students_Perc_Apr19_2019'].fillna(0)
df_joined['Applications_1819_Complete_Students_Perc_Apr19_2018'] = df_joined['Applications_1819_Complete_Students_Perc_Apr19_2018'].fillna(0)

df_joined['Applications_1920_Submitted_Students_Perc_Apr19_2019'] = df_joined['Applications_1920_Submitted_Apr19_2019'] / df_joined['Students']
df_joined['Applications_1819_Submitted_Students_Perc_Apr19_2018'] = df_joined['Applications_1819_Submitted_Apr19_2018'] / df_joined['Students']
df_joined['Applications_1920_Submitted_Students_Perc_Apr19_2019'] = df_joined['Applications_1920_Submitted_Students_Perc_Apr19_2019'].fillna(0)
df_joined['Applications_1819_Submitted_Students_Perc_Apr19_2018'] = df_joined['Applications_1819_Submitted_Students_Perc_Apr19_2018'].fillna(0)

df_joined['City'] = df_joined['City_x']
df_joined['State'] = df_joined['State_x']
df_joined.drop('County Name*', axis=1, inplace=True)
df_joined.drop('City_x', axis=1, inplace=True)
df_joined.drop('City_y', axis=1, inplace=True)
df_joined.drop('State_x', axis=1, inplace=True)
df_joined.drop('State_y', axis=1, inplace=True)
df_joined.drop('Name', axis=1, inplace=True)
df_joined.drop('Students*', axis=1, inplace=True)
df_joined.drop('Teachers*', axis=1, inplace=True)
df_joined.drop('Student Teacher Ratio*', axis=1, inplace=True)

df_joined.rename(columns={
    'Low Grade*': 'Low_Grade',
    'High Grade*': 'High_Grade',
    'Locale Code*': 'Locale_Code',
    'Locale*': 'Locale',
    'Magnet*': 'Magnet',
    'Title I School*': 'Title_I_School',
    'Title 1 School Wide*': 'Title_1_School_Wide',
    'Free Lunch*': 'Free_Lunch',
    'Reduced Lunch*': 'Reduced_Lunch'
}, inplace=True)

df_joined['High_Grade'] = df_joined['High_Grade'].astype('int8')
df_joined['Low_Grade'] = df_joined['Low_Grade'].astype('int8')
df_joined['Grades'] = df_joined['High_Grade'] - df_joined['Low_Grade'] + 1

"""## Checking Values

We want to check the possible unique values of all the categorical variables so we can get a better idea of the data structure.

First up is Free Lunch and Reduced Lunch, according to the data download, `–` means that data was missing and `†` means that data didn't meet the quality standards. If all we have in a column is missing data and zeros, we likely are not going to get any meaningful information from that column.
"""

print(df_joined['Free_Lunch'].unique())
print(df_joined['Reduced_Lunch'].unique())
print(df_joined['State'].unique())

# Since all that's in the Free_Lunch and Reduced_Lunch columns is '-' and 0, we'll just drop them.
df_joined.drop('Free_Lunch', axis=1, inplace=True)
df_joined.drop('Reduced_Lunch', axis=1, inplace=True)
df_joined.drop('State', axis=1, inplace=True)

print(df_joined['City'].unique())
print(df_joined['County'].unique())
print(df_joined['Magnet'].unique())
print(df_joined['Charter'].unique())
print(df_joined['Locale'].unique())
print(df_joined['Locale_Code'].unique())
print(df_joined['Title_I_School'].unique())
print(df_joined['Title_1_School_Wide'].unique())
print(df_joined['Grades'].unique())

"""## Graphs of Predictor Variables

Lets do some neat count graphs to see the spread of certain categories!
"""

ax_charter = sns.countplot(x='Charter', data=df_joined, palette=sns.cubehelix_palette(3, start=2))

ax_magnet = sns.countplot(x='Magnet', data=df_joined, palette=sns.cubehelix_palette(3, start=2))

ax_title_I_school = sns.countplot(x='Title_I_School', data=df_joined, palette=sns.cubehelix_palette(3, start=2))

ax_title_1_school_wide = sns.countplot(x='Title_1_School_Wide', data=df_joined, palette=sns.cubehelix_palette(3, start=2))

ax_locale = sns.countplot(y='Locale', data=df_joined, palette=sns.cubehelix_palette(8, start=2))

ax_locale_code = sns.countplot(y='Locale_Code', data=df_joined, palette=sns.cubehelix_palette(8, start=2))

ax_grades = sns.countplot(x='Grades', data=df_joined, palette=sns.cubehelix_palette(8, start=2))

ax_county = sns.countplot(y='County', data=df_joined, palette=sns.cubehelix_palette(24, start=2))

ax_students = sns.distplot(df_joined['Students'], axlabel="Students")

ax_teachers = sns.distplot(df_joined['Teachers'], axlabel="Teachers")

ax_student_teacher_ratio = sns.distplot(df_joined['Student_Teacher_Ratio'], axlabel="Student Teacher Ratio")

"""## Checking Correlation for Similar Columns"""

df_joined['Locale_Code_Coded'] = df_joined['Locale_Code'].astype('category').cat.codes
df_joined['Locale_Coded'] = df_joined['Locale'].astype('category').cat.codes

# Checking the correlation between Locale category and Locale Code
print(df_joined.corr()['Locale_Coded']['Locale_Code_Coded'])

df_joined.drop('Locale_Coded', axis=1, inplace=True)
df_joined.drop('Locale_Code_Coded', axis=1, inplace=True)

"""Looks like `Locale_Code` isn't just a duplicate of `Locale`, so they both get to stay in! For the actual analysis though, I'll have to one hot encode them.

Lets do that now (one-hot encode all the categorical variables)! I do plan on label encoding "Yes" to 1 and "No" to 0 for the ones that are only Yes and No, and don't have any missing data.

## Encoding Categories

This is important because typically categories aren't able to be processed rawly by most algorithms and techniques, so we need to convert them to a numerical value.

### Label Encoding

First lets encode the Yes and No categories as int8, which can be properly processed by machine learning algorithms.
"""

df_joined['Charter'] = df_joined['Charter'].map({'Yes': 1, 'No': 0}).astype('int8')
df_joined['Magnet'] = df_joined['Magnet'].map({'Yes': 1, 'No': 0}).astype('int8')
df_joined['Title_I_School'] = df_joined['Title_I_School'].map({'Yes': 1, 'No': 0}).astype('int8')
print(df_joined['Charter'].unique())
print(df_joined['Magnet'].unique())
print(df_joined['Title_I_School'].unique())

"""Nice! That worked out nicely. Now lets move on to the other categories.

### One-Hot Encoding

One-hot encoding converts each category to a 1 or 0 in its own column. Very useful for machine learning and data science techniques as it converts categories without possibly losing information like you can in label encoding with n > 2.
"""

df_joined['Locale_Code'] = df_joined['Locale_Code'].astype('category')
df_joined['ZIP'] = df_joined['ZIP'].astype('category')
df_joined['City'] = df_joined['City'].astype('category')
df_joined['District'] = df_joined['District'].astype('category')
df_joined['County'] = df_joined['County'].astype('category')
df_joined = df_joined.join(pd.get_dummies(df_joined[['Title_1_School_Wide', 'Locale', 'Locale_Code', 'ZIP', 'City', 'District', 'County']]))

print(df_joined.columns.tolist())

"""That's a lot of columns, but we need to delete all the columns we're not going to use in our analysis like the school ids and school codes."""

# Drop all the ones we one-hot encoded
df_joined.drop('Title_1_School_Wide', axis=1, inplace=True)
df_joined.drop('Locale', axis=1, inplace=True)
df_joined.drop('Locale_Code', axis=1, inplace=True)
df_joined.drop('ZIP', axis=1, inplace=True)
df_joined.drop('City', axis=1, inplace=True)
df_joined.drop('District', axis=1, inplace=True)
df_joined.drop('County', axis=1, inplace=True)

# Drop all the unneccessary columns.
df_joined.drop('Phone', axis=1, inplace=True)
df_joined.drop('ZIP 4-digit', axis=1, inplace=True)
df_joined.drop('Street Address', axis=1, inplace=True)
df_joined.drop('School Name', axis=1, inplace=True)
df_joined.drop('NCES School ID', axis=1, inplace=True)
df_joined.drop('State School ID', axis=1, inplace=True)
df_joined.drop('NCES District ID', axis=1, inplace=True)
df_joined.drop('State District ID', axis=1, inplace=True)

def pretty_density_plot(titles, texta=(1, "right")):
    sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    
    df_temp = df_joined[titles]

    df_temp = pd.melt(df_temp, id_vars=[], var_name='Year', value_name="Students")
    
    # Initialize the FacetGrid object
    pal = sns.cubehelix_palette(len(titles), start=2)
    g = sns.FacetGrid(df_temp, row="Year", hue="Year", aspect=15, height=1, palette=pal)

    # Draw the densities in a few steps
    g.map(sns.kdeplot, "Students", clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
    g.map(sns.kdeplot, "Students", clip_on=False, color="w", lw=2, bw=.2)
    g.map(plt.axhline, y=0, lw=2, clip_on=False)


    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(texta[0], .2, label.replace('_', ' '), fontweight="bold", color=color,
            ha=texta[1], va="center", transform=ax.transAxes)
    
    g.map(label, "Students")

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-.25)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[])
    g.despine(bottom=True, left=True)

raw_cols = ['Applications_1920_Submitted_Apr19_2019',
            'Applications_1920_Complete_Apr19_2019',
            'Applications_1819_Submitted_Apr19_2018',
            'Applications_1819_Complete_Apr19_2018',
            'Applications_1819_Submitted_Jun_2018',
            'Applications_1819_Complete_Jun_2018',
            'Applications_1819_Submitted_Dec_2018',
            'Applications_1819_Complete_Dec_2018']
pretty_density_plot(raw_cols, (1, "right"))

perc_cols =  ['Applications_1920_Complete_Students_Perc_Apr19_2019',
              'Applications_1819_Complete_Students_Perc_Apr19_2018',
              'Applications_1920_Submitted_Students_Perc_Apr19_2019',
              'Applications_1819_Submitted_Students_Perc_Apr19_2018',
             'Applications_1920_Completed_Submitted_Perc_Apr19_2019',
              'Applications_1819_Completed_Submitted_Perc_Apr19_2018']
pretty_density_plot(perc_cols, (.9, "left"))

ax_completed_2019 = sns.distplot(df_joined['Applications_1920_Completed_Submitted_Perc_Apr19_2019'], axlabel="19-20 Completed / Submitted")

ax_completed_2018 = sns.distplot(df_joined['Applications_1819_Completed_Submitted_Perc_Apr19_2018'], axlabel="18-19 Completed / Submitted")

"""## Data Descriptions

Lets get some basic statisics about the data so we can put that in our analysis.
"""

df_joined[raw_cols].describe()

df_joined[perc_cols].describe()

predictor_cols = df_joined.columns.difference(perc_cols+raw_cols)
print(predictor_cols)

"""## Now for Some Machine Learning

I'm first going to try applying a LightGBM model to the dataset, as I'll then be able to get feature importances so I can remove not useful ones. LightGBM is also fairly fast for how powerful it is, so I should be able to train it fairly quickly.

First, I'm going to setup some handy functions to do it for us.
"""

import lightgbm as lgb
from sklearn.metrics import mean_squared_error

# Taken from: https://github.com/Microsoft/LightGBM/blob/master/examples/python-guide/simple_example.py
def lightgbm_train_and_predict(X_train, X_test, y_train, y_test):
    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

    # specify your configurations as a dict
    params = {
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'metric': {'l2', 'l1'},
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0
    }
#     gbm = lgb.LGBMModel(params,
#                 lgb_train,
#                 num_boost_round=1000,
#                 valid_sets=lgb_eval,
#                 early_stopping_rounds=100)
    print('Starting training...')
    # train
    gbm = lgb.train(params,
                lgb_train,
                num_boost_round=1000,
                valid_sets=lgb_eval,
                early_stopping_rounds=100, verbose_eval=10)

    print('Saving model...')
    # save model to file
    gbm.save_model('model.txt')

    print('Starting predicting...')
    # predict
    y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
    # eval
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    print('The rmse of prediction is:', rmse)
    return gbm, rmse

rmse_for_target = {}
def split_and_train(target, predictors=predictor_cols):
    X_train, X_test, y_train, y_test = train_test_split(df_joined[predictors], df_joined[target], test_size=0.33, random_state=1337)
    print("Split done, calling trainer")
    model, rmse = lightgbm_train_and_predict(X_train, X_test, y_train, y_test)
    print("Done! Printing feature importances...")
    rmse_for_target[target] = rmse
    feat_importances = pd.Series(model.feature_importance(), index=predictors)
    feat_importances.nlargest(15).plot(kind='barh')
    return rmse

"""Now we need to actually do the training, we'll do the training with all values, then we'll try only taking the most important of each and train again.

### Percentages

#### First Iteration
"""

RMSE_full_features_percentage = []

RMSE_full_features_percentage.append(split_and_train('Applications_1920_Submitted_Students_Perc_Apr19_2019'))

RMSE_full_features_percentage.append(split_and_train('Applications_1819_Submitted_Students_Perc_Apr19_2018', predictors=predictor_cols.difference(['Income_2019'])))

RMSE_full_features_percentage.append(split_and_train('Applications_1920_Complete_Students_Perc_Apr19_2019'))

RMSE_full_features_percentage.append(split_and_train('Applications_1819_Complete_Students_Perc_Apr19_2018', predictors=predictor_cols.difference(['Income_2019'])))

sum(RMSE_full_features_percentage) / len(RMSE_full_features_percentage)

"""Looks like it's actually pretty accurate considering how low the RMSE is. The average RMSE error is about 3.56% which is pretty good considering that's within one standard deviation of the mean for all the statistics we described above for percentage. Now lets try it with only the good features.

#### Good features
"""

RMSE_top_features_percentage = []

RMSE_top_features_percentage.append(split_and_train('Applications_1920_Submitted_Students_Perc_Apr19_2019', predictors=['Title_I_School', 
                                                                                    'Income_2017', 
                                                                                    'Income_2018', 
                                                                                    'Income_2019', 
                                                                                    'Students', 
                                                                                    'Student_Teacher_Ratio', 
                                                                                    'Teachers',
                                                                                    'Locale_Code_21',
                                                                                    'Title_1_School_Wide_†',
                                                                                    'Title_1_School_Wide_Yes', 
                                                                                    'Magnet']))

"""So, not much improvement, still within one std. deviation and only a slight (`.0002`) improvement by only using the important features. Weird that `Income_2019` dropped to being very unimportant, though I expected `Charter` not to mean much. Still weird that `Locale_Code_21` was **so** important. It makes me really wonder what it represents."""

RMSE_top_features_percentage.append(split_and_train('Applications_1819_Submitted_Students_Perc_Apr19_2018', predictors=['Title_I_School', 
                                                                                    'Income_2017', 
                                                                                    'Income_2018', 
                                                                                    'Students', 
                                                                                    'Student_Teacher_Ratio', 
                                                                                    'Teachers',
                                                                                    'Locale_Suburb: Large',
                                                                                    'Locale_Code_21',
                                                                                    'Title_1_School_Wide_†',
                                                                                    'Title_1_School_Wide_Yes', 
                                                                                    'Magnet']))

"""This percentage model also got a small boost from only using important features, as we'd expect it to do so. Around the same gain as the previous one. Nothing terribly unexpected in the feature importances."""

RMSE_top_features_percentage.append(split_and_train('Applications_1920_Complete_Students_Perc_Apr19_2019', predictors=['Title_I_School', 
                                                                                    'Income_2017', 
                                                                                    'Income_2018', 
                                                                                    'Students', 
                                                                                    'Student_Teacher_Ratio', 
                                                                                    'Teachers',
                                                                                    'Locale_Suburb: Large',
                                                                                    'Locale_Code_21',
                                                                                    'Title_1_School_Wide_†',
                                                                                    'Title_1_School_Wide_Yes', 
                                                                                    'Magnet', 
                                                                                    'Income_2019',
                                                                                    'Locale_Code_41']))

RMSE_top_features_percentage.append(split_and_train('Applications_1819_Complete_Students_Perc_Apr19_2018', predictors=['Title_I_School', 
                                                                                    'Income_2017', 
                                                                                    'Income_2018', 
                                                                                    'Students', 
                                                                                    'Student_Teacher_Ratio', 
                                                                                    'Teachers',
                                                                                    'Locale_Suburb: Large',
                                                                                    'Locale_Code_21',
                                                                                    'Title_1_School_Wide_†',
                                                                                    'Title_1_School_Wide_Yes', 
                                                                                    'Magnet']))

sum(RMSE_top_features_percentage)/len(RMSE_top_features_percentage)

"""Slight improvement overall on the average RMSE for the percentage ones. Now we're going to try the raw numbers.

### Raw Numbers

I expect for the raw numbers, the column `Students` will be one of the most important for every run, as the algorithm not only has to predict how many students will interact with the FAFSA but also how many students the school has as a whole. It's also possible because of that it will care about the `Grades` feature, which was one I engineered by subtracting `Low_Grade` from `High_Grade`.

#### All Features
"""

RMSE_full_features_raw = []

RMSE_full_features_raw.append(split_and_train('Applications_1920_Submitted_Apr19_2019'))

"""A RMSE of 34.38 is actually pretty good considering the standard deviation for this data is in the 90's. As I predicted, the"""

RMSE_full_features_raw.append(split_and_train('Applications_1920_Complete_Apr19_2019'))

RMSE_full_features_raw.append(split_and_train('Applications_1819_Submitted_Apr19_2018', predictors=predictor_cols.difference(['Income_2019'])))

RMSE_full_features_raw.append(split_and_train('Applications_1819_Complete_Apr19_2018', predictors=predictor_cols.difference(['Income_2019'])))

"""Weird that `Locale_Suburb: Large` dropped off the features on this experiment. It's not terribly different than all the others so I'd expect it to show up here."""

sum(RMSE_full_features_raw) / len(RMSE_full_features_raw)

"""So `35.02188` isn't bad considering the standard deviation of most of the data is in the 90's. Now lets limit it to the top features and see if we can get an improvement. We probably will see at least **some** improvement, considering that's usually the case with boosting.

Also noteworthy is that the top feature of each model was students, as I predicted it might be.

#### Top Features
"""

RMSE_top_features_raw = []

RMSE_top_features_raw.append(split_and_train('Applications_1920_Submitted_Apr19_2019', predictors=['Title_I_School', 
                                                                                                    'Income_2017', 
                                                                                                    'Income_2018', 
                                                                                                    'Students', 
                                                                                                    'Student_Teacher_Ratio', 
                                                                                                    'Teachers',
                                                                                                    'Locale_Suburb: Large',
                                                                                                    'Locale_Code_21',
                                                                                                    'Title_1_School_Wide_†',
                                                                                                    'Title_1_School_Wide_Yes', 
                                                                                                    'Magnet',
                                                                                                    'City_Baltimore']))

"""Wow. I'm very surprised that `City_Baltimore` completely dropped off the map when we only used the top features, while `Locale_Suburb: Large` gained a couple of spots in the top features. This actually did slightly worse that the all features, though is still within the same ballpark."""

RMSE_top_features_raw.append(split_and_train('Applications_1920_Complete_Apr19_2019', predictors=['Title_I_School', 
                                                                                                    'Income_2017', 
                                                                                                    'Income_2018', 
                                                                                                    'Students', 
                                                                                                    'Student_Teacher_Ratio', 
                                                                                                    'Teachers',
                                                                                                    'Locale_Suburb: Large',
                                                                                                    'Locale_Code_21',
                                                                                                    'Title_1_School_Wide_†',
                                                                                                    'Title_1_School_Wide_Yes', 
                                                                                                    'Magnet',
                                                                                                    'City_Baltimore',
                                                                                                    'Locale_Code_41',
                                                                                                    'Income_2019']))

"""Not unexpected to see the `Locale_Code_41` drop off the top features list when we limit the number of features. Though it is quite weird to see `Locale_Code_21`, which was rather high previously drop all the way down."""

RMSE_top_features_raw.append(split_and_train('Applications_1819_Submitted_Apr19_2018', predictors=['Title_I_School', 
                                                                                                    'Income_2017', 
                                                                                                    'Income_2018', 
                                                                                                    'Students', 
                                                                                                    'Student_Teacher_Ratio', 
                                                                                                    'Teachers',
                                                                                                    'Locale_Suburb: Large',
                                                                                                    'Locale_Code_21',
                                                                                                    'Title_1_School_Wide_†',
                                                                                                    'Title_1_School_Wide_Yes', 
                                                                                                    'Magnet']))

"""Weird seeing `Title_1_School_Wide_Cross` drop so low from where it was above."""

RMSE_top_features_raw.append(split_and_train('Applications_1819_Complete_Apr19_2018', predictors=['Title_I_School', 
                                                                                                    'Income_2017', 
                                                                                                    'Income_2018', 
                                                                                                    'Students', 
                                                                                                    'Student_Teacher_Ratio', 
                                                                                                    'Teachers',
                                                                                                    'Locale_Code_21',
                                                                                                    'Title_1_School_Wide_†',
                                                                                                    'Title_1_School_Wide_Yes', 
                                                                                                    'Magnet']))

sum(RMSE_top_features_raw)/len(RMSE_top_features_raw)

"""**Wow!** Very surprising to see that the average root mean squared error went up in the better features. That's atypical of most boosting models."""