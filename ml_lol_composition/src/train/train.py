#Import libraries
import pandas as pd
import numpy as np

#Import algotirhms and functions
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

#Pre-processing data
df = pd.read_csv("./src/data/diamond_matches.csv")
df = df.drop(columns=['gameId']) 

df = df[['blueTotalGold', 'blueGoldDiff', 'blueTotalExperience', 'blueExperienceDiff', 'blueWardsPlaced', 'blueWins']] #Features 
x = df.drop(columns=['blueWins']) 
y = df['blueWins'] #Target variable

#Training models1
xgb_model = XGBClassifier(eval_metric='logloss', tree_method="hist")
xgb_model.fit(x, y)

y_pred = xgb_model.predict(x)
accuracy = accuracy_score(y, y_pred)

models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
}

kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42) 

for name, model in models.items():
    scores = cross_val_score(model, x, y, cv=kf, scoring="accuracy") #Using Cross-validation
    print(f'Accuracy using K-Fold Cross Validation ({name}):', np.mean(scores))

#Create Cross-Validation for XGBoost
score_xg = cross_val_score(model, x, y, cv=kf, scoring='accuracy')
print(f'Accuracy using K-Fold Cross Validation (XGBoost): ', np.mean(score_xg))

#Testing Model
match_example = {
    "blueTotalGold": 12000,
    "blueGoldDiff": 1200,
    "blueExperienceDiff": 100,
    "blueWardsPlaced": 6,
    "blueTotalExperience": 14000
}
print("Match Example:", match_example)
