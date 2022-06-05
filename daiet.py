from json import load
from turtle import shape
import numpy as np
import pandas as pd
import re


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
'''
The nutrient thresholds are taken directly from the Philippine Dietary Reference Intakes 2015
https://www.fnri.dost.gov.ph/images/images/news/PDRI-2018.pdf
'''
#(male, female) <- (0,1)

#fat is computed based on protein
#1-2 yrs: 6-15 -> 25:35
#3-18 yrs: 6-15 -> 15-30
#19 onwards: 10-15 -> 15-30

'''
Loads the recipes from the database. The default database
is the "Epicurious - Recipes with Rating and Nutrition" database
from https://www.kaggle.com/datasets/hugodarwood/epirecipes
Units: calories - Cal, fat - g, protein - g, sodium - mg
'''

class User:
    age_floor = [1,3,6,10,13,16,19,30,40,50,60,70] #lower bound of each age group
    calories = [(1000,920),(1350,1260),(1600,1470),(2060,1980),(2700,2170),(3010,2280),(2530,1930),(2420,1870),(2420,1870),(2140,1610),(1960,1540)]
    protein = [(18,17),(22,21),(30,29),(43,46),(62,57),(72,61),(71,62),(71,62),(71,62),(71,62),(71,62)]
    fat = [(i[0]*0.58,i[1]*0.58) for i in protein]
    fiber = [(i,i) for i in [7,10,14,17,20,23,25,25,25,25,25]]
    sodium = [(i,i) for i in [225,300,400,500,500,500,500,500,500,500,500]]
    carbohydrates = []
    cholesterol = []
    sugar = []

    pregmod = {"calories":300, "protein":27,"fat":0,"fiber":0,"sodium":0,}
    lacmod = {"calories":500, "protein":27,"fat":0,"fiber":0,"sodium":0,}
    threshold_table = {"calories":calories, "protein":protein,"fat":fat,"fiber":fiber,"sodium":sodium,}
    threshold_units = {"calories":"kcal", "protein":"g","fat":"g","fiber":"g","sodium":"mg",}

    def __init__(self, age = 20, sex = "male", preg = 0, lac = 0):
        self.update_status(age, sex, preg)

    def update_status(self,age,sex,preg,lac):
        self.age = age
        self.sex = (0 if sex.lower() in ["0","male","m"] else 1)
        self.pregnant = (1 if preg.lower() in ["1","pregnant","yes","y"] else 0)
        self.pregnant = (1 if preg.lower() in ["1","lactating","yes","y"] else 0)
        self.age_group = -1
        for i in range(len(self.age_floor)):
            if self.age_floor[i] <= self.age_group:
                self.age_group += 1
        self.update_threshold()

    def update_threshold(self, nutrients = ["calories","fat","protein","sodium"]):
        self.threshold = {}
        for i in nutrients:
            self.threshold[i] = self.threshold_table[i][self.age_group][self.sex] + self.pregnant*self.pregmod[i] + self.lactating*self.lacmod[i]
        print(self.threshold)
def searchmeal(rec_data, rec_attr, user):
    #PRIORITY: IMPLEMENT THIS
    '''
    
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
    '''
    pass

#terminal based text user interface
def text_ui(rec_data, rec_attr):

    user = User(input("Please input your age."), input("Please input your biological sex."), input("Are you pregnant?"),input("Are you lactating?"))
    print(str(rec_data.shape[0])+" recipes loaded with "+str(rec_data.shape[1])+" attributes")
    print(rec_data)
    print(rec_attr)
    while True:
        print("Current parameters:")
        print("Age = "+str(user.age))
        print("[1] Generate a new set of meals.")
        print("[2] Select nutrients to monitor.")
        print("[3] Adjust your excluded meals.")
        print("[4] Generate a new set of meals.")
        print("[5] Generate a new set of meals.")
        print("[6] Generate a new set of meals.")
        print("[Other] Exit dAIet.")
        choice = input("Select an option:")
        if choice == 1:
            print("Generating your meals...")
            meals = searchmeal(rec_data, rec_attr, user)
        else:
            print("Exiting daIet...")
            exit()

def load_recipes(recipe_path = "recipestest.json"):
    features = ["directions","fat","date","categories","calories","desc","protein","rating","title","ingredients","sodium"]
    nutrition = ["calories","protein","fat","sodium"]
    recipes = pd.read_json(recipe_path)
    recipes = recipes.dropna(subset = ["calories","protein","fat","sodium"])
    return recipes,nutrition
    

#load database and launch text ui
def main():
    rec_data, rec_attr = load_recipes()
    text_ui(rec_data)




if __name__ == "main":
    print("Welcome to dAIet. Opening text interface now...")
    main()