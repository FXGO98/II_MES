-- SQLite
--pragma foreign_keys = on;

drop table if exists orders;
create table orders
(
    orderId integer primary key,
    timestamp default current_timestamp not null
);

drop table if exists transformOrders;
create table transformOrders
(
    transformOrderId integer primary key,
    fromPiece text not null,
    toPiece text not null,
    qty integer not null,
    deadline timestamp,
    currStatus text not null
    --foreign key (transformOrderId) references orders(orderId)
);