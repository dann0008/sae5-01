with source_data_departement as (

    select *
    from departement
    where region in (select id
                     from "1_region_traite")

)

select *
from source_data_departement
