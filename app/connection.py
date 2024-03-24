import psycopg2
# Pour des raisons de sécurité en raisons de la réalisation du projet sur machine personnel, le mot de passe ne sera
# jamais précisé
db = psycopg2.connect(host="localhost", port=5432, user="dann0008", password="sae5-01", database="sae5-01")
cursor = db.cursor()
