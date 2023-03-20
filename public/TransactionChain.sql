create table "TransactionChain"
(
    "Transaction_ID" integer not null
        constraint transactionchain_pk
            primary key,
    "Sender_ID"      text,
    "Recipient_ID"   text,
    "Amount"         text,
    "Date"           text,
    "Time"           text,
    "New_Hash"       text,
    "Previous_Hash"  text
);

alter table "TransactionChain"
    owner to blakebabikianbentley;

