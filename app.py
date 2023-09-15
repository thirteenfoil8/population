from flask import Flask, jsonify, render_template, request
from psycopg2 import connect
from datetime import datetime

# Connexion à la base de données
conn = connect(dbname="simulation_db", user="user", password="password", host="db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS simulations (
        id SERIAL PRIMARY KEY,
        prenom VARCHAR(50),
        annee INT,
        population BIGINT,
        taux_de_natalite FLOAT,
        taux_de_mortalite FLOAT,
        timestamp TIMESTAMP
    )
''')
conn.commit()

app = Flask(__name__, template_folder='templates')

# État initial de la simulation
simulation_state = {
    "année": 2023,
    "population": 1000000,
    "taux_de_natalité": 0.012, 
    "taux_de_mortalité": 0.009,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/init', methods=['GET'])
def init():
    global simulation_state
    simulation_state = {
        "année": 2023,
        "population": 1000000,
        "taux_de_natalité": 0.012,
        "taux_de_mortalité": 0.009,
    }
    return jsonify(simulation_state), 200

@app.route('/avancer', methods=['GET'])
def avancer():
    global simulation_state
    # Mise à jour de la population en fonction des taux de natalité et de mortalité
    nouvelle_population = simulation_state["population"] + (simulation_state["population"] * simulation_state["taux_de_natalité"]) - (simulation_state["population"] * simulation_state["taux_de_mortalité"])
    simulation_state["population"] = nouvelle_population
    simulation_state["année"] += 1
    return jsonify(simulation_state), 200

@app.route('/etat', methods=['GET'])
def etat():
    global simulation_state
    return jsonify(simulation_state), 200

@app.route('/sauvegarder', methods=['POST'])
def sauvegarder():
    global simulation_state
    prenom = request.form['prenom']
    try:
        cursor.execute('''
            INSERT INTO simulations (prenom, annee, population, taux_de_natalite, taux_de_mortalite)
            VALUES (%s, %s, %s, %s, %s)
        ''', (prenom, simulation_state["année"], simulation_state["population"], simulation_state["taux_de_natalité"], simulation_state["taux_de_mortalité"]))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Une erreur s'est produite lors de la sauvegarde", "error": str(e)}), 400
    return jsonify({"message": "Simulation sauvegardée"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
