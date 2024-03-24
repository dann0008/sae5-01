import requests
import json
from app.city import city
import unidecode


class weather:

    def __init__(self, db, cursor, epci):
        self.db = db
        self.cursor = cursor
        self.epci = epci

    # Requête sur l'api météorologique pour une journée donnée afin de récupérer des informations météos sur les EPCIS
    # présent dans la liste transmise lors de la création de la classe afin d'en extraire certaines informations pour
    # les insérer dans la base de données après les avoirs modifier pour en calculer la moyenne  sur le nombre
    # d'aparition de l'EPCI dans les données de la journée, on ajoute également les EPCIS et Villes abscente de la liste
    # avec la méthode EPCIManquant de la classe city

    def ajoutCondition(self, date):
        uri = f'https://public.opendatasoft.com/api/records/1.0/search/?dataset=donnees-synop-essentielles-omm&q=&rows=550&refine.date={date}'
        response = requests.get(uri)
        weather = response.json()
        epci = []
        lst_epci = []
        weather2 = []
        suppression = []
        for record in weather['records']:
            if 'nom_epci' in record['fields']:
                weather2.append(record)

        for record in weather2:
            nom = unidecode.unidecode(record['fields']['nom_epci']).replace('\'', '`')
            if nom in ['CA Mont-de-Marsan Agglomeration', 'CC de Belle-Ile-en-Mer']:
                nom = nom.replace('-', ' ')
            if nom == 'CA Cap Excellence':
                nom = 'CA CAP Excellence'
            if nom not in self.epci:
                code_region = record['fields']['code_reg']
                nom_region = record['fields']['nom_reg'].replace('\'', '`')
                code_departement = record['fields']['code_dep']
                nom_departement = record['fields']['nom_dept'].replace('\'', '`')
                cityClass = city(self.db, self.cursor, self.epci)
                self.epci = cityClass.EPCIManquant(nom, code_region, nom_region, code_departement, nom_departement)
            lst_epci.append(nom)

        for EPCI in self.epci:
            if EPCI not in lst_epci:
                suppression.append(EPCI)

        for val in suppression:
            self.epci.remove(val)

        while len(epci) != len(self.epci):
            count_pression = 0
            pression = 0
            count_humidite = 0
            humidite = 0
            count_vitesse_vent = 0
            vitesse_vent = 0
            count_visibilite = 0
            visibilite = 0
            count_nebulosite = 0
            nebulosite = 0
            count_precipitation = 0
            precipitation = 0
            count_temperature = 0
            temperature = 0
            count_rafale = 0
            rafale = 0
            courant = None

            for record in weather2:
                flag = False
                if unidecode.unidecode(record['fields']['nom_epci']).replace('\'', '`') not in epci and courant is None:
                    courant = unidecode.unidecode(record['fields']['nom_epci']).replace('\'', '`')
                    epci.append(courant)
                    if courant in ['CA Mont-de-Marsan Agglomeration', 'CC de Belle-Ile-en-Mer']:
                        courant = courant.replace('-', ' ')
                        flag = True
                    if courant == 'CA Cap Excellence':
                        courant = 'CA CAP Excellence'
                        flag = True
                if unidecode.unidecode(record['fields']['nom_epci']).replace('\'', '`') == courant or flag:
                    if 'pmer' in record['fields']:
                        count_pression += 1
                        pression += record['fields']['pmer']
                    if 'u' in record['fields']:
                        count_humidite += 1
                        humidite += record['fields']['u']
                    if 'ff' in record['fields']:
                        count_vitesse_vent += 1
                        vitesse_vent += record['fields']['ff']
                    if 'vv' in record['fields']:
                        count_visibilite += 1
                        visibilite += record['fields']['vv']
                    if 'n' in record['fields']:
                        count_nebulosite += 1
                        nebulosite += record['fields']['n']
                    if 'rr6' in record['fields']:
                        count_precipitation += 1
                        precipitation += record['fields']['rr6']
                    if 'rafper' in record['fields']:
                        count_rafale += 1
                        rafale += record['fields']['rafper']
                    if 'tc' in record['fields']:
                        count_temperature += 1
                        temperature += record['fields']['tc']

            if pression != 0 and count_pression != 0:
                pression /= count_pression
                pression /= 100
                pression = round(pression, 2)
            else:
                pression = 'Nan'

            if humidite != 0 and count_pression != 0:
                humidite /= count_humidite
                humidite = round(humidite, 1)
            else:
                humidite = 'Nan'

            if vitesse_vent != 0 and count_vitesse_vent != 0:
                vitesse_vent /= count_vitesse_vent
                vitesse_vent *= 3.888
                vitesse_vent = round(vitesse_vent, 1)
            else:
                vitesse_vent = 'Nan'

            if visibilite != 0 and count_visibilite != 0:
                visibilite /= count_visibilite
                visibilite = int(round(visibilite, 0))
            else:
                visibilite = 0

            if nebulosite != 0 and count_nebulosite != 0:
                nebulosite /= count_nebulosite
                nebulosite = int(round(nebulosite, 0))
            else:
                nebulosite = 0

            if precipitation != 0 and count_precipitation != 0:
                precipitation /= count_precipitation
                precipitation = round(precipitation, 1)
                if precipitation < 0 or precipitation == 0:
                    precipitation = 'Nan'
            else:
                precipitation = 'Nan'

            if rafale != 0 and count_rafale != 0:
                rafale /= count_rafale
                rafale *= 3.888
                rafale = round(rafale, 1)
            else:
                rafale = 'Nan'

            if temperature != 0 and count_temperature != 0:
                temperature /= count_temperature
                temperature = round(temperature, 1)
            elif temperature == 0:
                pass
            else:
                temperature = 'Nan'

            self.cursor.execute(f"SELECT id from EPCI WHERE nom= '{courant}'")
            id_epci = self.cursor.fetchone()

            self.cursor.execute(f"INSERT INTO ConditionMeteo (pression, humidite, vitesseVent, visibilite, nebulosite,"
                                f"precipitation, rafale, temperature, date, epci) VALUES"
                                f"('{pression}', '{humidite}', '{vitesse_vent}', '{visibilite}', '{nebulosite}', "
                                f"'{precipitation}', '{rafale}', '{temperature}', '{date}', '{id_epci[0]}')")
            self.db.commit()

        return self.epci
