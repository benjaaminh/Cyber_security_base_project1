# Cyber security Base 2023 Course Project 1
This project is using the OWASP 2021 [top ten list](https://owasp.org/www-project-top-ten/) and CSRF

To run the project, install the [required dependencies](https://cybersecuritybase.mooc.fi/installation-guide) used in the course, clone the repository and run the command:

```
python manage.py runserver
```

The website has a superuser, with username superuser and password superuser

However, there are also default users:
   | Username | Password |
   |:--------:|:--------:|
   | admin    | admin |
   | bob   | squarepants |

## Flaw 1: [CSRF](https://cybersecuritybase.mooc.fi/module-2.3/1-security)
Source links pinpointing flaw 1:

Cross-site request forgery (CSRF) allows attackers to send requests to the target through another source where the attacker is authenticated. The victim may click a link that sends them to a malicious website, which in turn performs commands to actions that may steal or manipulate the victims data. In a website which is vulnerable to CSRF, the malicious commands can be planted in a HTML img tag which in turn runs the command instead of displaying an image. In my project, user bob has a note with a link. When the link is opened, csrf.html is opened and bob's password changes due to the url in the img tag. Some applications only validate the token when the request uses the POST method but skip the validation when the GET method is used. The application uses GET instead of POST to change password, meaning the csrf.html page will be able to change the password without csrf token

To fix this, we can add {% csrf_token %} to the forms where csrf token is missing to add the protection, as well as changing the GET request to POST request.


Flaw 2:
Broken access control. Users can change each others passwords without logging in.

Flaw 3: 
SQL injection, in adding a note

Flaw 4: Logging

Flaw 5: security misconfiguration
The settings.py file is visible for all, meaning the secret key will also be.
Since debug is set to TRUE, hackers could run the command python manage.py check --deploy, to see all vulnerabilities and potentially gain access to the program thisway. 
