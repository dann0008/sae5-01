with source_data_conditionmeteo as (

    select id, pression, humidite, precipitation, temperature, date, epci 
    from conditionmeteo
    where epci in (select id
                    from "5_epci_traite")

)

select *
from source_data_conditionmeteo
