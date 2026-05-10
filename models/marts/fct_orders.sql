with orders as (
    select * from {{ ref('stg_orders') }}
),

final as (
    select
        order_key,
        customer_key,
        order_status,
        total_price,
        order_date,
        order_priority,
        case
            when order_status = 'F' then true
            else false
        end as is_fulfilled
    from orders
)

select * from final
