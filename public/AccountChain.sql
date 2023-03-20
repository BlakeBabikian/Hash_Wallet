create table "AccountChain"
(
    "User_ID"    integer not null
        constraint accountchain_pk
            primary key,
    "First_Name" text,
    "Last_Name"  text,
    "Password"   text,
    "Balance"    text
);

alter table "AccountChain"
    owner to blakebabikianbentley;

create index id_index
    on "AccountChain" ("User_ID");

