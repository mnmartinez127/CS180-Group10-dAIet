import numpy as np
import pandas as pd
import re

'''
The nutrient thresholds are taken directly from the Philippine Dietary Reference Intakes 2015
https://www.fnri.dost.gov.ph/images/images/news/PDRI-2018.pdf
'''
#(male, female) <- (0,1)

#fat is computed based on protein
#1-2 yrs: 6-15 -> 25:35
#3-18 yrs: 6-15 -> 15-30
#19 onwards: 10-15 -> 15-30


def get_target(age = 20,s = 0):
    age_range = [0,0.5,1,3,6,10,13,16,19,30,40,50,60,70] #lower bound of each age group
    cal = [(620,560),(720,630),(1000,920),(1350,1260),(1600,1470),(2060,1980),(2700,2170),(3010,2280),(2530,1930),(2420,1870),(2420,1870),(2140,1610),(1960,1540)]
    protein = [(9,8),(17,15),(18,17),(22,21),(30,29),(43,46),(62,57),(72,61),(71,62),(71,62),(71,62),(71,62),(71,62)]
    fat = [(i[0]*0.58,i[1]*0.58) for i in protein]
    sodium = [120,200,225,300,400,500,500,500,500,500,500,500,500]
    pregmod = [300,27,0,0]
    lacmod = [500,27,0,0]
    for i in range(len(age_range)):
        if age_range[i] >= age:
            return [cal[i][s],protein[i][s],fat[i][s],sodium[i]]
    return [0,0,0,0]




'''
Loads the recipes from the database. The default database
is the "Epicurious - Recipes with Rating and Nutrition" database
from https://www.kaggle.com/datasets/hugodarwood/epirecipes
Units: calories - Cal, fat - g, protein - g, sodium - mg
'''
def load_data(recipe_path = "recipestest.json"):
    features = ["directions","fat","date","categories","calories","desc","protein","rating","title","ingredients","sodium"]
    nutrition = ["calories","protein","fat","sodium"]
    recipes = pd.read_json(recipe_path)
    recipes = recipes.dropna(subset = ["title","calories","protein","fat","sodium"])
    return recipes
a = load_data()[["title","calories","protein","fat","sodium"]]
print(a)

target = get_target()
threshold = target.copy()
print(target)
food = []
limit = 1.0
mincost = None
for i,row in a.iterrows():
    print("food "+str(i)+": "+str(row["title"])+" -> "+str((row["calories"]-target[0]))+" -> "+str((row["protein"]-target[1]))+" -> "+str((row["fat"]-target[2]))+" -> "+str((row["sodium"]-target[3])))
    cost = abs(row["calories"]-target[0]) * abs(row["protein"]-target[1]) * abs(row["fat"]-target[2]) * abs(row["sodium"]-target[3])
    print("cost: "+str(cost))
    if row["calories"] < (threshold[0]*limit) and row["protein"] < (threshold[1]*limit) and row["fat"] < (threshold[2]*limit) and row["sodium"] < (threshold[3]*limit):
        print("Valid item")
        if mincost is None:
            mincost = [i,row["title"],cost]
        elif mincost[2] > cost:
            mincost = [i,row["title"],cost]
print(mincost)
#load database
#select categories
#filter nutritional info
#divide by category



'''
search parameters:
food type (meat, chicken, fish, pasta, soup, ...)
number of dishes for a day

start with 1 dish (random)
for each round:
    select a random category,
    traverse category for a dish that minimizes cost
    if cost threshold is reached, stop search
    if dish threshold is reached, 

'''