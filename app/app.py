from flask import Flask, jsonify, render_template, request
from psycopg2 import connect
import pickle
import pandas as pd

data = pd.read_csv('data/data.csv')
country_names = data['Name'].dropna().unique().tolist()

# Chargez la liste all_CCA3
with open('data/all_CCA3.pkl', 'rb') as f:
    all_CCA3 = pickle.load(f)

# Charger le modèle
with open('data/model.pkl', 'rb') as f:
    model = pickle.load(f)

def get_population_from_1970(country_name):
    country_data = data[data['Name'] == country_name]
    return int(country_data['1970'].values[0])

# Connexion à la base de données
conn = connect(dbname="simulation_db", user="user", password="password", host="db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS simulations (
        id SERIAL PRIMARY KEY,
        prenom VARCHAR(50),
        annee INT,
        population BIGINT,
        timestamp TIMESTAMP
    )
''')
conn.commit()

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# État initial de la simulation
simulation_state = {
    "année": 1970,
    "population": 1000000,
}



@app.route('/get_country_data', methods=['GET'])
def get_country_data():
    global simulation_state  
    country_name = request.args.get('country_name')
    population_1970 = get_population_from_1970(country_name)
    simulation_state = {
        "année": 1970,
        "pays": country_name,
        "population": population_1970,  # Remplacez par la vraie population de 1970 pour le pays spécifié
    }
    return jsonify(simulation_state)

@app.route("/", methods=['GET', 'POST'])
def index():
    # Pour obtenir la population de 1970 pour le pays par défaut
    default_country_name = "France"  # par exemple, pour la France
    default_population = get_population_from_1970(default_country_name)
    return render_template('index.html',
                            default_population=default_population,
                            default_country_name=default_country_name,
                            country_names=country_names)

@app.route('/select_country', methods=['POST'])
def select_country():
    global simulation_state
    selected_country = request.form['country']
    simulation_state["année"] = 1970
    simulation_state["population"] = get_population_from_1970(selected_country)
    return jsonify(simulation_state), 200

@app.route('/init', methods=['GET'])
def init():
    global simulation_state
    simulation_state = {
        "année": 1970,
        "population": 1000000
    }
    return jsonify(simulation_state), 200

@app.route('/avancer', methods=['GET'])
def avancer():
    country_name = request.args.get('country')
    cca3_code = data.loc[data['Name'] == country_name, 'CCA3'].values[0]
    # Préparez les données pour la prédiction
    input_data = pd.DataFrame([{
        'CCA3': cca3_code,  # Remplacez par le CCA3 du pays que vous voulez prédire
        'Year': simulation_state['année'],  # Utilisez l'année de l'état de la simulation
    }])

    # Fixez les catégories CCA3 et effectuez un encodage one-hot
    input_data['CCA3'] = input_data['CCA3'].astype('category').cat.set_categories(all_CCA3)
    input_data = pd.get_dummies(input_data, columns=['CCA3'], drop_first=True)

    # Utilisez le modèle pour faire une prédiction
    prediction = model.predict(input_data)
    print(prediction[0])
    
    # Mettez à jour l'état de la simulation avec la prédiction
    simulation_state['population'] = prediction[0]
    simulation_state['année'] += 1

    return jsonify(simulation_state), 200

@app.route('/sauvegarder', methods=['POST'])
def sauvegarder():
    global simulation_state
    prenom = request.form['prenom']
    try:
        cursor.execute('''
            INSERT INTO simulations (prenom, annee, population)
            VALUES (%s, %s, %s)
        ''', (prenom, simulation_state["année"], simulation_state["population"]))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Une erreur s'est produite lors de la sauvegarde", "error": str(e)}), 400
    return jsonify({"message": "Simulation sauvegardée"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
