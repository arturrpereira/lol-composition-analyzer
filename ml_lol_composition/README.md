# Models

That topic was created to make models and predict the champions taht will be choiced based the enemy composition and what champions they choiced.

The first model trained named "ml_one".

The unique file was uploaded it's the "train.py", that contains the training of the model.

# Dependeces

The libraries used in the project it on requirements.txt, that marked the version of the libraries used to made the first model.

Certify that you have installed Python and Pip if you are on Windows, or installed Python if you are on Linux System.

- To use the Script training, you need to install the Python libraries. If you are on Windows, you need to run:

    ~~~bash
        pip install pandas
        pip install scikit-learn
        pip install xgboost
- The numpy librarie it's install with pandas, so you don't need to run a command to be used it.

- Now, if you on Linux System, you run the commands with sudo apt:

    ~~~bash
    sudo apt install pandas
    sudo apt install xgboost
    sudo apt install 
- Check the versions of the libraries if you have any problem with the execution and if the errors relation with them.

# Use the Script Training

- Now, with all dependences installed, you can open the terminal and run:
    ~~~bash 
    python3 train.py
- The output will be similar to this:
    ~~~Out
    Accuracy using K-Fold Cross Validation (Logistic Regression): 0.7264913134833189
    Accuracy using K-Fold Cross Validation (Decision Tree): 0.6278980679546968
    Accuracy using K-Fold Cross Validation (Random Forest): 0.7046275303643725
    Accuracy using K-Fold Cross Validation (XGBoost):  0.7082710500691846
    Match Example: {'blueTotalGold': 12000, 'blueGoldDiff': 1200, 'blueExperienceDiff': 100, 'blueWardsPlaced': 6, 'blueTotalExperience': 14000}