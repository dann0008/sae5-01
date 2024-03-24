class database:

    def __init__(self, cursor):
        self.cursor = cursor

    # Suppression de toutes les Tables de la base de données en début d'éxécution de l'application avant de la recréer
    # avec la méthode creation

    def suppression(self):

        self.cursor.execute("""
                    DROP TABLE IF EXISTS "6_conditionmeteo_traite";
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS "5_epci_traite";
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS "4_personne_traite";
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS "3_ville_traite";
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS "2_departement_traite";
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS "1_region_traite";
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS ConditionMeteo;
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS Personne;
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS Ville;
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS EPCI;
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS Departement;
                """)

        self.cursor.execute("""
                    DROP TABLE IF EXISTS Region;
                """)

    # Création de toutes les Tables de la base de données après l'exécution de la méthode suppression

    def creation(self):

        self.suppression()

        self.cursor.execute("""
           
           CREATE TABLE Region (
            id INT PRIMARY KEY NOT NULL,
            nom VARCHAR(30) NOT NULL
            );
        """)

        self.cursor.execute("""
           
           CREATE TABLE Departement (
             code VARCHAR(3) PRIMARY KEY NOT NULL,
             nom VARCHAR(30) NOT NULL,
             region INT NOT NULL,
             CONSTRAINT FK_DepartementRegion FOREIGN KEY (region) REFERENCES Region(id)
             );
        """)

        self.cursor.execute("""
        
           CREATE TABLE EPCI (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(50) NOT NULL,
            departement VARCHAR(3),
            CONSTRAINT FK_EPCIDepartement FOREIGN KEY (departement) REFERENCES Departement(code)
            );
        """)

        self.cursor.execute("""
        
            CREATE TABLE Ville (
             id SERIAL PRIMARY KEY,
             nom VARCHAR(50) NOT NULL,
             code_postal VARCHAR(5) NOT NULL,
             departement VARCHAR(3) NOT NULL,
             epci INT NOT NULL,
             CONSTRAINT FK_VilleDepartement FOREIGN KEY (departement) REFERENCES Departement(code),
             CONSTRAINT FK_VilleEPCI FOREIGN KEY (epci) REFERENCES EPCI(id)
              );
        """)

        self.cursor.execute("""
        
            CREATE TABLE Personne (
             id SERIAL PRIMARY KEY,
             sexe BOOLEAN NOT NULL,
             dateNais DATE NOT NULL,
             dateDeces DATE NOT NULL,
             age INT NOT NULL,
             ville INT NOT NULL,
             CONSTRAINT FK_PersonneVille FOREIGN KEY (ville) REFERENCES Ville(id)
              );
        """)

        self.cursor.execute("""
        
            CREATE TABLE ConditionMeteo (
             id SERIAL PRIMARY KEY,
             pression FLOAT,
             humidite FLOAT,
             vitesseVent FLOAT,
             visibilite INT,
             nebulosite INT,
             precipitation FLOAT,
             rafale FLOAT,
             temperature FLOAT,
             date DATE NOT NULL,
             epci INT NOT NULL,
             CONSTRAINT FK_ConditionMeteoEPCI FOREIGN KEY (epci) REFERENCES EPCI(id)
              );
        """)
