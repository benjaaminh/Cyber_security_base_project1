# Cyber security Base 2023 Course Project 1
This project is using the OWASP 2021 [top ten list](https://owasp.org/www-project-top-ten/) and CSRF

To run the project, install the [required dependencies](https://cybersecuritybase.mooc.fi/installation-guide) used in the course, clone the repository and run the command:

```
python manage.py runserver
```
The website can be found at http://127.0.0.1:8000/ once the server is up and running

The website has a superuser, with username superuser and password superuser

However, there are also default users:
   | Username | Password |
   |:--------:|:--------:|
   | admin    | admin |
   | bob   | squarepants |

## Flaw 1: [CSRF](https://cybersecuritybase.mooc.fi/module-2.3/1-security)
Source links pinpointing flaw 1:
CSRF tokens: https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/notes/templates/pages/index.html#L39C1-L39C1, 

https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/notes/templates/pages/index.html#L47C1-L47C1,

csrf_exempt: https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/notes/views.py#L14C22-L14C22 

GET requests: https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/notes/templates/pages/index.html#L46,

https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/notes/views.py#L37-L38

Cross-site request forgery (CSRF) allows attackers to send requests to the target through another source where the attacker is authenticated. The victim may click a link that sends them to a malicious website, which in turn performs commands to actions that may steal or manipulate the victims data. In a website which is vulnerable to CSRF, the malicious commands can be planted in a HTML img tag which in turn runs the command instead of displaying an image. In my project, user bob has a note with a link. When the link is opened, csrf.html is opened and bob's password changes due to the url in the img tag. Some applications only validate the token when the request uses the POST method but skip the validation when the GET method is used. The application uses GET instead of POST to change password, meaning the csrf.html page will be able to change the password without CSRF token

To fix this, we can add {% csrf_token %} to the forms where CSRF token is missing in index.html to add the protection, as well as changing the GET request to POST request in both index.html: 
https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/notes/templates/pages/index.html#L46


and views.py: https://github.com/benjaaminh/Cyber_security_base_project1/blob/344264279e75e7959b7ab49e0d6a092d6974056f/cybersecurityproject/notes/views.py#L35-L36

as well as removing @csrf_exempt from views.py in adding notes: https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/notes/views.py#L14C22-L14C22 


## Flaw 2: [Broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
Source links pinpointing flaw 2: https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/notes/views.py#L37-L38, 
https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/notes/templates/pages/index.html#L46C2-L46C2, 
https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/notes/views.py#L33 

With broken access control, restriction on what users are allowed to do is not implemented. The web application can store data through e.g a path variable. The variable can be modified which in turn allows the user to gain access to data that they shouldnt be able to access. The program may not check for authorization, allowing users with basic privileges access administrative features. Weak authentication, such as weak password policies or lack of multi-factor authentication is also included in broken access control. In this application, users are able to change eachothers passwords. They can also change passwords without logging in. Opening the link http://localhost:8000/changepassword/?user=bob&password=hacked while the server is running will change user bob's password to hacked. 

To fix this, we should change the GET requests in flaws linked to POST requests (which in turn requires CSRF tokens to be enabled), to hide the parameters in the url. So, add CSRF tokens in index.html as in the fix to flaw 1 and remove @csrf_exempt from views.py: 
CSRF tokens: https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/notes/templates/pages/index.html#L39C1-L39C1, 

https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/notes/templates/pages/index.html#L47C1-L47C1,

csrf_exempt: https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/notes/views.py#L14C22-L14C22 

And change GET to POST request: 
index.html: 
https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/notes/templates/pages/index.html#L46


and views.py: https://github.com/benjaaminh/Cyber_security_base_project1/blob/344264279e75e7959b7ab49e0d6a092d6974056f/cybersecurityproject/notes/views.py#L35-L36 

Also, we should add the @login_required above the changing password view, so users can't change passwords without logging in: https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/notes/views.py#L33 

## Flaw 3: [SQL injection](https://owasp.org/Top10/A03_2021-Injection/)
Source links pinpointing flaw 3: https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/notes/views.py#L22 

SQL injection allows attackers to inject malicious data into a user-input field due to unsanitized user inputs. The parameters given into the user input contains an SQL query which in turn manipulates the database used in the web application. With the SQL query, attackers can delete or modify data and access passwords and other sensitive data. In this application, the function for adding notes is done with an SQL query INSERT INTO, where the parameters are not properly sanitized. Attackers can put their SQL queries into the same field for adding a note to manipulate the database.

To fix this, we should instead use django's standard method of creating objects with models: 
https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/notes/views.py#L16-L18



## Flaw 4: [Logging](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)

Source links pinpointing flaw 4: https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/notes/views.py#L8, 
https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/cybersecurityproject/settings.py#L134 

Without proper logging, system administrators will not be able to detect activity in the web application. When a password is changed, the system administrator is not able to see the change. An attacker could change another user's password without the system administrator noticing any suspicious activity. 

To fix this, We can implement logging using django's built in logging to help system administrators detect any suspicious activity. With logging, any suspicious action is logged for the system administrator to see. 

Source links pinpointing fixes to flaw 4:

Logging in views.py: https://github.com/benjaaminh/Cyber_security_base_project1/blob/344264279e75e7959b7ab49e0d6a092d6974056f/cybersecurityproject/notes/views.py#L9-L11 
And logging in settings.py: 
https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/cybersecurityproject/settings.py#L135-L167 

## Flaw 5: [Security misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)

Source links pinpointing flaw 5: 
SECRET_KEY visible: https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/cybersecurityproject/settings.py#L29 
DEBUG=True: https://github.com/benjaaminh/Cyber_security_base_project1/blob/8c9cc64e1216055c29cd7c05a37185fc66f24af9/cybersecurityproject/cybersecurityproject/settings.py#L32C13-L32C13 

With security misconfiguration, we refer to oversights or errors in the configuration of the application. Security might not have been taken into account while configuring the application. A security misconfiguration can lead to a vulnerable application, allowing hackers to access the application more easily. In this application, 
the settings.py file has the secret key visible for all. The secret key is used to encrypt and decrypt sensitive information, which is why it should be hidden. Since debug is set to TRUE, hackers could run the command
```python manage.py check --deploy``` , to see all vulnerabilities and potentially gain access to the program this way. 

To fix the security misconfiguration, we should fix the issues mentioned by the console when running the previous command while debug=TRUE and fix them. To hide the secret key, we should put it in a .env file, step by step:  

1. To hide the secret key, we will need to install a new dependency by running the command in the console: 

```pip install python-dotenv```

2. Afterwards, create a new .env file in the base directory (same as manage.py): https://github.com/benjaaminh/Cyber_security_base_project1/blob/main/cybersecurityproject/.env

3. And put the .env file into the .gitignore file, so version control won't detect it, since the file includes the secret key: https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/.gitignore#L1-L2 The secret key will be saved on the computer locally. 


4. Import dotenv library in settings.py:https://github.com/benjaaminh/Cyber_security_base_project1/blob/master/cybersecurityproject/cybersecurityproject/settings.py#L15 
and load key: https://github.com/benjaaminh/Cyber_security_base_project1/blob/main/cybersecurityproject/cybersecurityproject/settings.py#L24-L26

