create table sales (
    order_id int primary key,
    order_date date not null,
    customer_name varchar(100)not null,
    city varchar(50)not null,
    product varchar(100)not null,
    category varchar(50)not null,
    quantity int not null,
    unit_price numeric(10,2)not null,
    payment_method varchar(20)not null
);