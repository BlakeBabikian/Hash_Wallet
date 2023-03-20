create table "DepositChain"
(
    "Deposit_ID"   text not null
        constraint depositchain_pk
            primary key,
    "User_ID"      text,
    "Amount"       text,
    "Date"         text,
    "Time"         text,
    "Deposit Hash" text
);

alter table "DepositChain"
    owner to blakebabikianbentley;

