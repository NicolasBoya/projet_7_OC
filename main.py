from fastapi import FastAPI
import pickle
import pandas as pd
import numpy as np
import lightgbm as lgb
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, fbeta_score, make_scorer
from pydantic import BaseModel
#import joblib
from models_core import *

from sklearn.metrics import classification_report, balanced_accuracy_score, accuracy_score

# 2. Create the app and model objects
api = FastAPI(
    title="LGBM Prediction",
    description="Predict score",
    version="1.0.0")


#model = Predict()


lgbm_model = pickle.load(open('LGBM_best_model.pickle', 'rb'))
X_test = pickle.load(open('X_test_lgbm.pickle', 'rb'))
X_test = X_test.reset_index()
X_test = X_test.drop(['index'], axis=1)
print(X_test)
class ID_client(BaseModel):
    ID : int

#@api.get("/Test")
#async def test_titre():
#    return{"Veuillez entrer l'ID du client recherché"}

@api.post("/Test")
async def ask_id(id_client:ID_client):
    
    print("ask_id().   ----------------------------------------------------")
    find_client = X_test.iloc[id_client.ID]
    find_client = find_client.array.reshape(1, -1)
    print(find_client)
    probability = lgbm_model.predict_proba(find_client)[:,1] #probabilité
    prediction = lgbm_model.predict(find_client) #prediction
    print("-Probabilité--------------------------------------------------------------------")
    print(probability)
    
    print("-Prédiction---------------------------------------------------------------")
    print(prediction)
    
    print("--------------------------------------------------------------------------")
    
    output = pd.DataFrame({'prediction': prediction, 'probability': probability})
    return output.to_dict(orient = 'records')

@api.get("/test2/{a}/{b}")
async def compute_sum(a, b):
    return {'sum': int(a) + int(b)}

'''
@api.get("/")
async def hello_world():
    return{"hello world"}
    
@api.get("/Nicolas")
async def current_user():
    result = {
            'status' : 'success',
            'message' : (f"Hello ! Welcome to Fast API.")
        }
    return result
'''
#@api.post('/predict')
#async def make_predictions():
    
#    """
#    Effectuer des prédictions sur de nouvelles données en provenance d'un fichier pickle
#    """
#    return model.predict()


#Test

#def predict(test):
#    lgbm_model = pickle.load(open('LGBM_best_model.pickle', 'rb'))
    #X_test = pickle.load(open('X_test_lgbm.pickle', 'rb'))
    #X_test = X_test.reset_index()
    #X_test = X_test.drop(['index'], axis=1)
    #X_test = test_set.drop('SK_ID_CURR', axis=1)
#    probability = lgbm_model.predict_proba(test)#[:,1] #probabilité
#    prediction = lgbm_model.predict(test) #prediction

#    output = pd.DataFrame({'prediction': prediction[:10], 'probability': probability[:10]})

#    return output.to_dict(orient = 'records')