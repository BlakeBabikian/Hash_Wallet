# Hash_Wallet
Introduction:

During an intro to cloud computing class, I was introduced to a couple cryptography concepts.  One of these was hashing, it was interesting to me because it was cool to think that no matter the data inputted it will always produce, a unique hash.  Additionally, no matter how many times you do this hash, if the data is the same the hash is the same.  I had heard a lot about blockchain so I figured I would start a project that could use the tools I had learned. With my study abroad semester approaching I thought this would be a great way for me to continue to utilize my skills, outside of a classroom enviornment. 

The first step was to think of a practical application to apply this to, and since money is the means of most transactions, I figured I would make an atm/banking app.  I started out just making a python console app.  This is mostly because I did not know flask at the time, and front-end devolvement seemed daunting at the time.  The original app worked fine, but after a demo with several people, saying how cool the program was, I knew I needed to make a front end.

I had taken a www class, so HTML JS and CSS were already in my toolbox.  All I needed was flask to handle the mix of those with Python.  Flask syntax, looking at it not knowing it, is overwhelming.  I used ChatGPT to give me examples of how flask looks.  This was incredibly helpful in allowing me to go line by line on my main function on my original console program and transform it to a flask app. 

Originally all my data was stored on txt file, it was just a decision I made early on, once I thought about it more, I would prefer using csv’s. So, I did that, only to find out Heroku doesn't store csv's really well.  I then move to a Postgres database, using SQLAlchemy to utilize with my python.


Methods:

My program uses 3 python files:
App.py – Session Maker 
wsgi.py Flask App
backEnd.py – All my python
encrypt.py – My encryptor
database.py - Database interface code

13 HTML files

A Postgres DB
AccountChain – Accounts and balances
TransactionChain – A record of all the transactions
DepositChain - a record of all deposits
SessionChain - Login log

My logic behind my data security is:

I hash the transaction data (sender_id, receiver_id, amount, date, time, old_hash, new_hash)
All data is found on transaction csv

To audit this first I make sure the data in the row matches the hash, 
if someone changes the data without the hash these will not equal.
	If someone changes the data and the hash, the row will be valid, but the next row will 	not as its hash was made with the previous hash before the change.

Next, I make sure the new_hash is equal to the next chain links old hash,
This again forces a lot of data to be changed down the line in order for my audit functions to not pick up on it

Demo:

https://hash-wallet.herokuapp.com/

Create your account and sign in!

![image](https://user-images.githubusercontent.com/105388898/210686727-e0f13c3b-833c-4e79-8b32-f167d8926bfb.png)
