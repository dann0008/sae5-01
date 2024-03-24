with source_data_region as (

    select *
    from region
    where id between 94 and 6

)

select *
from source_data_region
