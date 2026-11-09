from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Il est recommandé de gérer la connexion dans chaque route ou via un pool de connexions 
# pour éviter les pertes de connexion, mais voici la correction basée sur votre structure.
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="ciel2027"
)

@app.route('/v1/etudiants/', methods=['GET'])
def getEtudiants():
    cursor = mydb.cursor()
    req = "SELECT * FROM etudiant"
    cursor.execute(req)
    result = cursor.fetchall()
    etudiants = []
    for row in result:
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }
        etudiants.append(etudiant)
    cursor.close()
    return jsonify(etudiants), 200

@app.route('/v1/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    cursor = mydb.cursor()
    req = "SELECT * FROM etudiant WHERE idetudiant = %s"
    cursor.execute(req, (id,))
    row = cursor.fetchone()
    cursor.close()
    
    if row:
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }
        return jsonify(etudiant), 200
    return jsonify({"erreur": "Etudiant non trouvé"}), 404

@app.route('/v1/etudiants/', methods=['POST'])
def addEtudiant():
    data = request.get_json()
    cursor = mydb.cursor()
    req = "INSERT INTO etudiant (nom, prenom, email, telephone) VALUES (%s, %s, %s, %s)"
    val = (data['nom'], data['prenom'], data['email'], data['telephone'])
    cursor.execute(req, val)
    mydb.commit()
    cursor.close()
    return jsonify("Ajout OK"), 201

@app.route('/v1/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    data = request.get_json()
    cursor = mydb.cursor()
    req = "UPDATE etudiant SET nom = %s, prenom = %s, email = %s, telephone = %s WHERE idetudiant = %s"
    val = (data['nom'], data['prenom'], data['email'], data['telephone'], id)
    cursor.execute(req, val)
    mydb.commit()
    cursor.close()
    return jsonify("Modification OK"), 200

@app.route('/v1/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    cursor = mydb.cursor()
    req = "DELETE FROM etudiant WHERE idetudiant = %s"
    cursor.execute(req, (id,))
    mydb.commit()
    cursor.close()
    return jsonify("Suppression OK"), 200

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug=True)
