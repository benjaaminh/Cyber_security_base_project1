# Cyber security Base 2023 Course Project 1
This project is using the OWASP 2021 [top ten list](https://owasp.org/www-project-top-ten/) and CSRF

To run the project, install the [required dependencies](https://cybersecuritybase.mooc.fi/installation-guide) used in the course, clone the repository and run the command:

```
python manage.py runserver
```
The website can be found at localhost:8000 once the server is up and running

The website has a superuser, with username superuser and password superuser

However, there are also default users:
   | Username | Password |
   |:--------:|:--------:|
   | admin    | admin |
   | bob   | squarepants |

## Flaw 1: [CSRF](https://cybersecuritybase.mooc.fi/module-2.3/1-security)
Source links pinpointing flaw 1:
CSRF tokens: https://github.com/benjaaminh/Cyber_security_base_project1/blob/1716a0434fd3123af35f6c43c673fd6c48cc7a0c/cybersecurityproject/notes/templates/pages/index.html#L39C32-L39C32,
https://github.com/benjaaminh/Cyber_security_base_project1/blob/1716a0434fd3123af35f6c43c673fd6c48cc7a0c/cybersecurityproject/notes/templates/pages/index.html#L47C6-L47C6
GET requests: 

Cross-site request forgery (CSRF) allows attackers to send requests to the target through another source where the attacker is authenticated. The victim may click a link that sends them to a malicious website, which in turn performs commands to actions that may steal or manipulate the victims data. In a website which is vulnerable to CSRF, the malicious commands can be planted in a HTML img tag which in turn runs the command instead of displaying an image. In my project, user bob has a note with a link. When the link is opened, csrf.html is opened and bob's password changes due to the url in the img tag. Some applications only validate the token when the request uses the POST method but skip the validation when the GET method is used. The application uses GET instead of POST to change password, meaning the csrf.html page will be able to change the password without csrf token

To fix this, we can add {% csrf_token %} to the forms where csrf token is missing in index.html to add the protection, as well as changing the GET request to POST request in both index.html: https://github.com/benjaaminh/Cyber_security_base_project1/blob/1716a0434fd3123af35f6c43c673fd6c48cc7a0c/cybersecurityproject/notes/templates/pages/index.html#L38C4-L38C4, https://github.com/benjaaminh/Cyber_security_base_project1/blob/1716a0434fd3123af35f6c43c673fd6c48cc7a0c/cybersecurityproject/notes/templates/pages/index.html#L46
and views.py: https://github.com/benjaaminh/Cyber_security_base_project1/blob/1716a0434fd3123af35f6c43c673fd6c48cc7a0c/cybersecurityproject/notes/views.py#L32C2-L33


## Flaw 2: [Broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
Source links pinpointing flaw 2: https://github.com/benjaaminh/Cyber_security_base_project1/blob/1716a0434fd3123af35f6c43c673fd6c48cc7a0c/cybersecurityproject/notes/views.py#L34C2-L35C39,
https://github.com/benjaaminh/Cyber_security_base_project1/blob/1716a0434fd3123af35f6c43c673fd6c48cc7a0c/cybersecurityproject/notes/templates/pages/index.html#L46

With broken access control, restriction on what users are allowed to do is not implemented. The web application can store data through e.g a path variable. The variable can be modified which in turn allows the user to gain access to data that they shouldnt be able to access. The program may not check for authorization, allowing users with basic privileges access administrative features. Weak authentication, such as weak password policies or lack of multi-factor authentication is also included in broken access control. In this application, users are able to change eachothers passwords. They can also change passwords without logging in. Opening the link http://localhost:8000/changepassword/?user=bob&password=hacked while the server is running will change user bob's password to hacked. 

To fix this, we should change the GET requests in both flaws linked to POST requests (which in turn requires CSRF tokens to be enabled), to hide the parameters in the url. Also, we should add the @login_required above the changing password view, so users can't change passwords without logging in.

## Flaw 3: [SQL injection](https://owasp.org/Top10/A03_2021-Injection/)
Source links pinpointing flaw 3: https://github.com/benjaaminh/Cyber_security_base_project1/blob/a7e4874dc20e3003d4a82d6bcd92422b5d3a5bba/cybersecurityproject/notes/views.py#L20C2-L20C2 

SQL injection allows attackers to inject malicious data into a user-input field due to unsanitized user inputs. The parameters given into the user input contains an SQL query which in turn manipulates the database used in the web application. With the SQL query, attackers can delete or modify data and access passwords and other sensitive data. In this application, the function for adding notes is done with an SQL query INSERT INTO, where the parameters are not properly sanitized. Attackers can put their SQL queries into the same field for adding a note to manipulate the database.

To fix this, we should instead use django's standard method of creating objects with models: 
https://github.com/benjaaminh/Cyber_security_base_project1/blob/a7e4874dc20e3003d4a82d6bcd92422b5d3a5bba/cybersecurityproject/notes/views.py#L14-L16 



Flaw 4: Logging

Flaw 5: security misconfiguration
The settings.py file is visible for all, meaning the secret key will also be.
Since debug is set to TRUE, hackers could run the command python manage.py check --deploy, to see all vulnerabilities and potentially gain access to the program thisway. 
