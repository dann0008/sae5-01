# Commande utilisé pour dbt

## Installation de dbt

    pip install dbt-postgres

    dbt --version

## Installation de PostGre

## Initialisation d'un projet dbt

    dbt init sae5_01

## Mise en place de la connexion

    sae5_01: 
      target: dev
      outputs:
        dev:
          type: postgres
          host: localhost
          user: dann0008
          password: sae5-01
          port: 5432
          dbname: SAE5-01 # or database instead of dbname
          schema: public #[dbt schema]

    
    dbt debug

## Exécution de dbt

    dbt run (vérification du bon fonctionnement de dbt)