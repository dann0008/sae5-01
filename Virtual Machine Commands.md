# Commande utilisé pour la création de la Machine Virtuel

## Mise à jour de la VM

    sudo apt update && sudo apt upgrade -y

## Mise en place du fonctionnement du sudo

    hostname

    nano /etc/hosts (ajout de la ligne 127.0.0.1 localhost.localdomain)

## Création d'un utilisateur

    useradd dann0008

    usermod -aG sudo dann0008

    sudo passwd dann0008

    mkdir /home/dann0008

    mkdir /home/dann0008/.ssh

    cp /root/.ssh/authorized_keys /home/dann0008/.ssh/ 

    chown dann0008 /home/dann0008/.ssh /home/dann0008/.ssh/authorized_keys

    redémarrage de la machine virtuel pour appliquer toutes les mises à jour

## Installation de Java

    apt install -y wget apt-transport-https

    mkdir -p /etc/apt/keyrings

    wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc
    
    echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list

    apt update

    apt install temurin-17-jdk

    java -version

## Téléchargement de fichier .JAR

    cd ..

    mkdir metabase

    cd metabase/

    wget https://downloads.metabase.com/v0.47.2/metabase.jar

## Lancement du l'exécution du fichier .JAR

    java -jar metabase.jar & (lancement en tache de fond) (PID = 2487)

## Accès à Metabase

    http://10.31.32.10:3000/

    Création d'un utilisateur :
        mail : lucas.danneaux@etudiant.univ-reims.fr
        password : sae5-01

## installation de PostgreSQL

    apt install postgresql postgresql-contrib

    systemctl start postgresql.service

## Configuration de PostGreSQL

    sudo -u postgres psql

    CREATE USER dann0008 WITH PASSWORD 'sae51';

    sudo -u postgres createdb sae5-01

## Installation du service apache2

    apt install apache2

## Installation de adminer

    apt install adminer

    a2enconf adminer.conf

    systemctl reload apache2

    10.31.32.183/adminer

    Connexion à la base de données :
        System : PostgreSQL
        Server : localhost
        Username : dann0008
        Password : sae51
        Database : sae5-01

## Installation de git

    git config --global user.email "lucas.danneaux@etudiant.univ-reims.fr"

    git config --global user.name "Lucas Danneaux"

    git config --global --list

## Récupération du dépot

    cd /

    git clone https://iut-info.univ-reims.fr/gitlab/dann0008/sae4-01-edition-postgresql.git

## Mise en place de l'application python

    cd sae4-01-edition-postgresql/

    apt install python3-pip

    apt-get install libpq-dev

    pip install -r requirements.txt

    nano app/connection.py (ajout des informations de connections à la base de données)

    python3 application.py & (PID = 15045)

## Ajout des données dans metabase

    Type : PostgreSQL
    Name : sae
    Host : localhost
    Port : 5432
    Database Name : sae5-01
    Username : dann0008
    Password : sae51
    Schemas : Tout

## Mise à jour de Metabase

Durant la réalisation de ce projet Metabase est passé en version 0.47.5, j'ai décidé de réaliser cette mise à jour afin de bénéficier des apports de cette dernière

    ps aux (PID = 2487)

    kill 2487

    cd /metabase/

    rm metabase.jar

    wget https://downloads.metabase.com/v0.47.5/metabase.jar

    java -jar metabase.jar & (PID = ?)

## En cas de problème de connexion ssh

    à exécuter en dehors de la machine virtuel dans notre Home

    ssh-keygen -f "/home/Users/dann0008/.ssh/known_hosts" -R "10.31.32.10"

    chmod -R 700 .ssh
