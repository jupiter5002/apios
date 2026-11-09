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


def login():
    auth = request.authorization
    if auth is None:
        return False
    username = auth.username
    password = auth.password

    req = f"SELECT * FROM user WHERE login = '{username}' AND password = '{password}'"
    cursor.execute(req)
    data = cursor.fetchone()
    if data:
        return True
    else:
        return False


@app.route('/v3/etudiants/', methods=['GET'])
def getEtudiants():
    if login():
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
    else:
        return jsonify("Acces refuse"), 401


@app.route('/v3/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    if login():
        req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
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
    else:
        return jsonify("Acces refuse"), 401


@app.route('/v3/etudiants/', methods=['POST'])
def addEtudiant():
    if login():
        data = request.get_json()
        req = f"INSERT INTO etudiant (nom, prenom, email, telephone) VALUES ('{data['nom']}', '{data['prenom']}', '{data['email']}', '{data['telephone']}')"
        cursor.execute(req)
        mydb.commit()
        return jsonify("Ajout OK"), 201
    else:
        return jsonify("Acces refuse"), 401


@app.route('/v3/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    if login():
        data = request.get_json()
        req = f"UPDATE etudiant SET nom = '{data['nom']}', prenom = '{data['prenom']}', email = '{data['email']}', telephone = '{data['telephone']}' WHERE idetudiant = {id}"
        cursor.execute(req)
        if cursor.rowcount == 0:
            return jsonify({'erreur': 'id invalide'}), 404
        mydb.commit()
        return jsonify("Modification OK"), 200
    else:
        return jsonify("Acces refuse"), 401


@app.route('/v3/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    if login():
        req = f"DELETE FROM etudiant WHERE idetudiant = {id}"
        cursor.execute(req)
        if cursor.rowcount == 0:
            return jsonify({'erreur': 'id invalide'}), 404
        mydb.commit()
        return jsonify("Suppression OK"), 200
    else:
        return jsonify("Acces refuse"), 401


if __name__ == "__main__":
    app.run(debug=True)

