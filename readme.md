users:
admin:admin
bob:squarepants

Flaw 1: CSRF
removed csrf token from index.html and login.html
Some applications correctly validate the token when the request uses the POST method but skip the validation when the GET method is used. 
tbc
todo: make csrf page for bob

Flaw 2:
Broken access control. Users can change each others passwords without logging in.

Flaw 3: 
SQL injection, in adding a note