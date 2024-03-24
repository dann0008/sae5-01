with source_data_ville as (

    select id, nom, epci
    from ville
    where departement in (select code
                          from "2_departement_traite")

)

select *
from source_data_ville
