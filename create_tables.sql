-- SQLite
--pragma foreign_keys = on;

drop table if exists orders;
CREATE TABLE orders
(
    orderId integer primary key,
    timestamp default current_timestamp not null
);

drop table if exists transformOrders;
CREATE TABLE transformOrders
(
    orderId integer primary key,
    fromPiece text not null,
    toPiece text not null,
    qty integer not null,
    deadline timestamp,
    currStatus text not null
    --foreign key (transformOrderId) references orders(orderId)
);

drop table if exists unloadOrder;
CREATE TABLE unloadOrder 
(
    orderId integer primary key,
    piece text not null,
    destination text not null,
    quantity integer not null,
    currStatus text not null
);

drop table if exists warehouse;
CREATE TABLE  warehouse 
(
    piece text not null primary key,
    quantity integer
); 

INSERT INTO warehouse (piece, quantity) VALUES ('P1', 54);
INSERT INTO warehouse (piece, quantity) VALUES ('P2', 54);
INSERT INTO warehouse (piece, quantity) VALUES ('P3', 54);
INSERT INTO warehouse (piece, quantity) VALUES ('P4', 54);
INSERT INTO warehouse (piece, quantity) VALUES ('P5', 54);
INSERT INTO warehouse (piece, quantity) VALUES ('P6', 54);
INSERT INTO warehouse (piece, quantity) VALUES ('P7', 54);
INSERT INTO warehouse (piece, quantity) VALUES ('P8', 54);
INSERT INTO warehouse (piece, quantity) VALUES ('P9', 54);

drop table if exists unloadStats;
CREATE TABLE unloadStats
        (
            zoneId integer primary key,
            P1 integer,
            P2 integer,
            P3 integer,
            P4 integer,
            P5 integer,
            P6 integer,
            P7 integer,
            P8 integer,
            P9 integer
        );

drop table if exists machineStats;
CREATE TABLE  machineStats
(
    machineId integer not null,
    machinetype text not null,
    tool integer not null,
    totaltime text,
    P1 integer,
    P2 integer,
    P3 integer,
    P4 integer,
    P5 integer,
    P6 integer,
    P7 integer,
    P8 integer,
    P9 integer
)


            