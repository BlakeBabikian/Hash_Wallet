create table "SessionChain"
(
    "Session_ID" integer not null
        constraint sessionchain_pk
            primary key,
    "User_ID"    integer,
    "Date"       text,
    "Time"       text
);

alter table "SessionChain"
    owner to blakebabikianbentley;

