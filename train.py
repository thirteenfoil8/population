import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from joblib import dump
import pickle

# Étape 1 & 2: Charger et préparer les données
data = pd.read_csv('data/data.csv')
years = [2022, 2020, 2015, 2010, 2000, 1990, 1980, 1970]
years_str = [str(year) for year in years]
df = data.melt(id_vars=['CCA3', 'Name'], value_vars=years_str, var_name='Year', value_name='Population')
df.dropna(subset="CCA3", inplace=True)

# Étape 3 : Créer le modèle
X = df[['CCA3', 'Year']]
y = df['Population']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Supposons que X_train et X_test sont vos dataframes d'entraînement et de test

# Obtenez la liste des colonnes CCA3 uniques dans le dataframe d'entraînement
unique_CCA3_train = X_train['CCA3'].unique()

# Obtenez une liste complète des CCA3 qui devraient être présents dans les deux ensembles
all_CCA3 = list(set(unique_CCA3_train) | set(X_test['CCA3'].unique()))


# Remplacez les valeurs manquantes dans les deux dataframes
X_train['CCA3'] = X_train['CCA3'].astype('category').cat.set_categories(all_CCA3)
X_test['CCA3'] = X_test['CCA3'].astype('category').cat.set_categories(all_CCA3)

# Effectuez l'encodage one-hot sur la colonne CCA3
X_train = pd.get_dummies(X_train, columns=['CCA3'], drop_first=True)
X_test = pd.get_dummies(X_test, columns=['CCA3'], drop_first=True)

# Entraînement du modèle
model = LinearRegression()
model.fit(X_train, y_train)

# Étape 4 : Tester le modèle
y_pred = model.predict(X_test)
with open('all_CCA3.pkl', 'wb') as f:
    pickle.dump(all_CCA3, f)


with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Évaluer la performance du modèle
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')