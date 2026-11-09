from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="ciel2027"
)

cursor = mydb.cursor()


@app.route('/v2/etudiants/', methods=['GET'])
def getEtudiants():
    try:
        etudiants = []
        req = "SELECT * FROM etudiant"
        cursor.execute(req)
        result = cursor.fetchall()
        for row in result:
            etudiant = {
                "idetudiant": row[0],
                "nom": row[1],
                "prenom": row[2],
                "email": row[3],
                "telephone": row[4]
            }
            etudiants.append(etudiant)
        return jsonify(etudiants), 200
    except mysql.connector.Error:
        return jsonify({'erreur': 'echec de connexion a la base de donnees'}), 500


@app.route('/v2/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
    print(req)
    try:
        cursor.execute(req)
        row = cursor.fetchone()
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }
        return jsonify(etudiant), 200
    except TypeError:
        return jsonify({'erreur': 'id invalide'}), 404


@app.route('/v2/etudiants/', methods=['POST'])
def addEtudiant():
    try:
        data = request.get_json()
        req = f"INSERT INTO etudiant (nom, prenom, email, telephone) VALUES ('{data['nom']}', '{data['prenom']}', '{data['email']}', '{data['telephone']}')"
        cursor.execute(req)
        mydb.commit()
        return jsonify("Ajout OK"), 201
    except mysql.connector.Error:
        return jsonify({'erreur': 'echec de connexion a la base de donnees'}), 500


@app.route('/v2/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    try:
        data = request.get_json()
        req = f"UPDATE etudiant SET nom = '{data['nom']}', prenom = '{data['prenom']}', email = '{data['email']}', telephone = '{data['telephone']}' WHERE idetudiant = {id}"
        cursor.execute(req)
        if cursor.rowcount == 0:
            return jsonify({'erreur': 'id invalide'}), 404
        mydb.commit()
        return jsonify("Modification OK"), 200
    except mysql.connector.Error:
        return jsonify({'erreur': 'echec de connexion a la base de donnees'}), 500


@app.route('/v2/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    try:
        req = f"DELETE FROM etudiant WHERE idetudiant = {id}"
        cursor.execute(req)
        if cursor.rowcount == 0:
            return jsonify({'erreur': 'id invalide'}), 404
        mydb.commit()
        return jsonify("Suppression OK"), 200
    except mysql.connector.Error:
        return jsonify({'erreur': 'echec de connexion a la base de donnees'}), 500


if __name__ == "__main__":
    app.run(debug=True)

