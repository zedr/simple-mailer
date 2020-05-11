# Simple Mailer
A simple Python mailer script that's suitable for Namecheap Shared Hosting.

[![Build Status](https://travis-ci.com/zedr/simple-mailer.svg?branch=master)](https://travis-ci.com/zedr/simple-mailer)

## Installation

### Namecheap Shared Hosting

1. Go to CPanel

2. Create a new Python application

3. In the "Create Application" wizard:

    3.1. Select Python version 3.7.3 or higher

    3.2. Choose a name for your Application root, e.g. simple-mailer

    3.3. Choose a path name for the Application URL, e.g. simple-mailer

    3.4. Leave the Application startup file field blank

    3.5. Leave the Application Entry point field blank

    3.6. Choose the name of the Passenger log file, e.g. simple-mailer.log

    3.7. Add a new Environment variable, with name `SMTP_HOST` and the host name
     of your chosen smtp server
    
    3.8. Add a new Environment variable, with name `SMTP_HOST` and the host name of your chosen smtp server, e.g. mail.smacznykaseksuwalki.com

    3.9. Add a new Environment variable, with name `SMTP_PORT` and the port number of your smtp server, e.g. 465

    3.10. Add a new Environment variable, with name `FROM_ADDRESS` and the name of your sender email address, e.g. mailer@example.com
    
    3.11. Add a new Environment variable, with name `TO_ADDRESS` and the name of your recipient email address, e.g. inbox@example.com

    3.12. Add a new Environment variable, with name `USE_TLS` and set it to `false` if you don't want secure communication to your SMTP server or it doesn't support it (not recommended) 

    3.13. Add a new Environment variable, with name `USE_TLS` and set it to `false` if you don't want secure communication to your SMTP server or it doesn't support it (not recommended) 

    3.14. Create the Application 

4. Connect via SSH to your Unix Shared hosting environment
    
    4.1 Activate the Virtual environment linked to you application, e.g
    
    4.2 `pip install simple-mailer`

    4.3 Edit the `passenger_wsgi.py` file in your application's home, e.g. `~/simple-mailer/passenger_wsgi.py`

    4.4. Replace the contents of the file so that it reads as follows:
    ```python
    import os
    import sys

    from simple_mailer.web import get_application

    sys.path.insert(0, os.path.dirname(__file__))

    application = get_application()
    ```
5. Start the application

6. Go to http://www.mydomain.com/simple-mailer and you should get the following response: `{"mailer": "/mail"}`. This indicates that the program has been installed correctly.

## Configuration

All configuration is done using environment variables.

### SMTP_HOST

The hostname of the SMTP server that will send the email.

Example: `smtp.example.com`

### SMTP_PORT

The port number of the SMTP server at `SMTP_HOST`.

Example: `465`

### USE_TLS

Secure the connection to the SMTP server using TLS. Highly recommended.

Default: `true`

### SMTP_USERID

The id of the SMTP user account on the SMTP server at `SMTP_HOST`.

Example: `mailer@example.com`

### SMTP_PASSWORD

The password of the SMTP user account on the SMTP server at `SMTP_HOST`.

Example: `rosebud20`

### TO_ADDRESS

The recipient email address that will receive the email.

Example: `orders@example.net`

### FROM_ADDRESS

The email address of the sender that will appear in the email that will 
be sent.

Example: `mailer@example.com`

### MAIL_SUBJECT

The subject of every sent email.

Example: `A new order has been received`

Default: An empty string.

TODO: Allow the use of fields.

### MAIL_TEMPLATE_PATH

The filesystem path to the email template file that will be used for the 
outgoing email.

Example: `/home/myuser/templates/mail.txt`

Default: The default template will be used.

### MAILER_PATH

The path of the URL where the mailer resource will be available.

Example: `my-mail`

Default: `mail`

If the root path of this application has been made available at 
`https://api.example.com/simple-mailer`, email will need to be POSTed to
`https://api.example.com/simple-mailer/my-mail`

### CAPTCHA

The captcha protocol to use.

Example: `recaptchav3`

Default: An empty string (no captcha system will be used - not recommended)

### CAPTCHA_SECRET

The secret used to validate the request using a given sercret.

Example: `d0n0tsh4r3m3`

Default: An empty string.

### CAPTCHA_VERIFY_URL

The URL where challenge responses regarding the captcha can be verified.

Example: `https://www.google.com/recaptcha/api/siteverify`

Default: An empty string.

### FIELDS_EXCLUDED

A list of fields in the POST request to exclude from the email. Fields are
comma separated.

Example: `secret_field1,secret_field2`

Default: An empty string (no fields are excluded)

TODO: strip border whitespace

TODO: Add `FIELDS_INCLUDED`
