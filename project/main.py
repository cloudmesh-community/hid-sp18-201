import numpy as np
import csv
import random
import math
from flask import Flask, request
from scipy.spatial import distance
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
import operator
#for rest service:
import requests
from flask import Flask
from sklearn.externals.joblib import Memory
from sklearn.datasets import load_svmlight_file
from sklearn.svm import SVC
from os import listdir
from flask import Flask, request


#Storing the file as 'data'
data = "new_movies.csv"

df = []
with open("new_movies.csv", 'r') as csvfile:
    df = pd.read_csv(csvfile)

#using file management to read in the file
file = open(data, "r")
#Keeping a count of the number of Movies with line numbering.
count = 0

#Creating empty lists for each of the variables
movie_name=[]
movie_month=[]
movie_day = []
movie_year = []
movie_budget = []
movie_domgross = []
movie_worldgross = []

for line in file:
    #print (count, line)
    #Increment the line number
    count = count+1
    words=line.split('\n')[0].split(',')
    movie_name.append(words[0])
    movie_month.append(words[1])
    movie_day.append(words[2])
    movie_year.append(words[3])
    movie_budget.append(words[4])
    movie_domgross.append(words[5])
    movie_worldgross.append(words[6])

movie_month_integer_value=[]
for month in movie_month:
    if month=='Jan':
        movie_month_integer_value.append(1)
    if month == 'Feb':
        movie_month_integer_value.append(2)
    if month == 'Mar':
        movie_month_integer_value.append(3)
    if month == 'Apr':
        movie_month_integer_value.append(4)
    if month == 'Mar':
        movie_month_integer_value.append(5)
    if month == 'Jun':
        movie_month_integer_value.append(6)
    if month == 'Jul':
        movie_month_integer_value.append(7)
    if month == 'Aug':
        movie_month_integer_value.append(8)
    if month == 'Sep':
        movie_month_integer_value.append(9)
    if month == 'Oct':
        movie_month_integer_value.append(10)
    if month == 'Nov':
        movie_month_integer_value.append(11)
    if month == 'Dec':
        movie_month_integer_value.append(12)


#Printing out Movie line by line with values.
'''
for i in range(len(movie_name)):
    count_str = (str)(i)
    print('NUMBER: ' + count_str+ ' ' + 'NAME: "'+movie_name[i]+
    '" RELEASE DATE: '+(str)(movie_month_integer_value[i])+
    '.'+movie_day[i]+'.'+movie_year[i]+' BUDGET: '+movie_budget[i]+'M'+' '+
    ' WORLD GROSS: '+movie_worldgross[i]+'M')
    print('\n')
    '''



#use pandas to make into table
#from numpy find random function
#random interval, give beginning and End
#pandas find 80% of items
#index = random movies
#training = original_Data[index]
#original_data[-index]

#Randomly pick a movie to add to the training set list.
#randomly sample 70% of the dataframe:
df_70 = df.sample(frac=0.7)
#get the rest of it:
df_rest = df.loc[~df.index.isin(df_70.index)]

training_data = df_70
test_data = df_rest
#print(df.columns.values)
selected_movie = df[df["ï»¿Movie"] == "Toy Story 3"].iloc[0]
distance_columns = ['Budget($M)', 'Domestic Gross($M)', 'Worldwide Gross($M)']
def euclidean_distance(row):
    inner_value = 0
    for k in distance_columns:
        inner_value += (row[k] - selected_movie[k]) ** 2
    return math.sqrt(inner_value)
avatar_distance = df.apply(euclidean_distance, axis = 1)
df_numeric = df[distance_columns]
df_normalized = (df_numeric - df_numeric.mean()) / df_numeric.std()
df_normalized.fillna(0, inplace = True)
avatar_normalized = df_normalized[df["ï»¿Movie"] == "Toy Story 3"]
euclidean_distances = df_normalized.apply(lambda row: distance.euclidean(row, avatar_normalized), axis = 1)
distance_frame = pd.DataFrame(data={"dist": euclidean_distances, "idx": euclidean_distances.index})
test = distance_frame.sort_values("dist")
#print((test))
second_smallest = test.iloc[1]["idx"]
most_similar_to_avatar = df.loc[int(second_smallest)]["ï»¿Movie"]
#print(most_similar_to_avatar)
def closest_to(movie_name):
    selected_movie = df[df["ï»¿Movie"] == movie_name].iloc[0]
    distance_columns = ['Budget($M)', 'Domestic Gross($M)', 'Worldwide Gross($M)']
    def euclidean_distance(row):
        inner_value = 0
        for k in distance_columns:
            inner_value += (row[k] - selected_movie[k]) ** 2
        return math.sqrt(inner_value)
    avatar_distance = df.apply(euclidean_distance, axis = 1)
    df_numeric = df[distance_columns]
    df_normalized = (df_numeric - df_numeric.mean()) / df_numeric.std()
    df_normalized.fillna(0, inplace = True)
    avatar_normalized = df_normalized[df["ï»¿Movie"] == movie_name]
    euclidean_distances = df_normalized.apply(lambda row: distance.euclidean(row, avatar_normalized), axis = 1)
    distance_frame = pd.DataFrame(data={"dist": euclidean_distances, "idx": euclidean_distances.index})
    test = distance_frame.sort_values("dist")
    second_smallest = test.iloc[1]["idx"]
    most_similar_to_avatar = df.loc[int(second_smallest)]["ï»¿Movie"]
    print("The movie most similar to " +movie_name+ " is: ")
    print(most_similar_to_avatar)
    return(most_similar_to_avatar)

#Function here to call
closest_to("Monsters, Inc.")


#App route beginning:
app = Flask(__name__)

def download_data(url, filename):
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)

def data_partition(filename, ratio):
    file = open(filename,'r')
    training_file=filename+'_train'
    test_file=filename+'_test'
    data = file.readlines()
    count = 0
    size = len(data)
    ftrain =open(training_file,'w')
    ftest =open(test_file,'w')
    for line in data:
        if(count< int(size*ratio)):
            ftrain.write(line)
        else:
            ftest.write(line)
        count = count + 1


@app.route('/')
def index():
    return "Sohile Ali E222 Final Project"
    print (closest_to("The Terminal"))




@app.route('/api/download/data')
def download():
    url = 'https://www.dropbox.com/s/ryshfakvbtrddd2/new_movies2.csv.xlsx?dl=0'
    download_data(url=url, filename='new_movies2.csv')
    return "Motion Picture Data Downloaded as 'new_movies2.csv' "



@app.route('/api/data/partition')
def partition():
    data_partition('new_movies2.csv',0.8)
    return "Motion Picture Data Successfully Partitioned"

#Dynamically Changing the movie
@app.route('/api/experiment/<name>')
def my_view_func(name):
    return closest_to(name)

if __name__ == '__main__':
    app.run(debug=True)
