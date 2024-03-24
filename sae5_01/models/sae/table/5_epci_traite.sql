with source_data_epci as (

    select *
    from epci
    where departement in (select code
                    from "2_departement_traite")

)

select *
from source_data_epci
