with source_data_personne as (

    select id, 
    case 
    when sexe = true THEN 'Homme'
    else 'Femme'
    end as "sexe", datedeces, age, ville
    from personne
    where ville in (select id
                    from "3_ville_traite")
    and age < 102

)

select *
from source_data_personne
