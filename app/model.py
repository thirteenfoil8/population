from joblib import load
import pandas as pd

model = load('model.joblib')

def predict_population(country_code, year):
    # Création d'un DataFrame avec les données d'entrée
    data = {'CCA3': [country_code], 'Year': [year]}
    df = pd.DataFrame(data)
    
    # Encodage one-hot pour la variable 'CCA3'
    df = pd.get_dummies(df, columns=['CCA3'], drop_first=True)
    
    # Prédiction de la population
    pred = model.predict(df)
    
    return pred[0]
