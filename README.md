# Simple Mailer
[![Build Status](https://travis-ci.com/zedr/simple-mailer.svg?branch=master)](https://travis-ci.com/zedr/simple-mailer)
[![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/download/releases/3.7.0/)
[![PyPi version](https://img.shields.io/pypi/v/simple-mailer.svg)](https://pypi.python.org/pypi/simple-mailer/)
![t](https://img.shields.io/badge/status-beta-orange.svg)

A simple Python mailer program that can be run in the WSGI environment of a
shared hosting provider.

This program provides a web resource that can be used by an HTML web form 
to send a plain text email to a specific email address.

### Features:
 - Can be triggered by a WSGI call or run standalone as a daemon
 - Configurable using environment variables
 - Captcha support (Recaptcha v3 for now)
 - Customizable email template
 - Easy to setup

## Installation
### Shared Hosting
1. Install the package, e.g. using `pip install simple-mailer`
2. Copy over the `wsgi/passenger_wsgi.py` to the appropriate folder and rename 
accordingly
3. Configure the environment variables, listed below, as needed

More information, including hosting provider specific instructions, can be
found on the [Wiki](https://github.com/zedr/simple-mailer/wiki).

## Configuration

All configuration is done using environment variables.

#### SMTP_HOST

The hostname of the SMTP server that will send the email.

Example: `smtp.example.com`

#### SMTP_PORT

The port number of the SMTP server at `SMTP_HOST`.

Example: `465`

#### USE_TLS

Secure the connection to the SMTP server using TLS. Highly recommended.

Default: `true`

#### SMTP_USERID

The id of the SMTP user account on the SMTP server at `SMTP_HOST`.

Example: `mailer@example.com`

#### SMTP_PASSWORD

The password of the SMTP user account on the SMTP server at `SMTP_HOST`.

Example: `rosebud20`

#### TO_ADDRESS

The recipient email address that will receive the email.

Example: `orders@example.net`

#### FROM_ADDRESS

The email address of the sender that will appear in the email that will 
be sent.

Example: `mailer@example.com`

#### MAIL_SUBJECT

The subject of every sent email.

You can use Jinja2 template tags here, just like the email body. The variables
in the template context are:
 - data, containing all the fields that were sent (and passed the filters)
 - metadata, containing fields for: client_ip (the originating IP address), 
   origin (the origin of the request, e.g. the page with the form),
   mailer_url (the URL of the mailer endpoint that processed the request)

Example: `An order for {{data.goods} was sent from IP {{metadata.client_ip}}`

Default: An empty string.

#### MAIL_TEMPLATE_PATH

The filesystem path to the email template file that will be used for the 
outgoing email.

You can use Jinja2 template tags in the email template. The variables that will
be made available in the template context are:
 - data, containing all the fields that were sent (and passed the filters)
 - metadata, containing fields for: client_ip (the originating IP address), 
   origin (the origin of the request, e.g. the page with the form),
   mailer_url (the URL of the mailer endpoint that processed the request)

Example: `/home/myuser/templates/mail.txt`

Default: The default template will be used.

#### MAILER_PATH

The path of the URL where the mailer resource will be available.

Default: `mail`

If the root path of this application has been made available at 
`https://api.example.com/simple-mailer`, email will need to be POSTed to
`https://api.example.com/simple-mailer/mail`

#### CAPTCHA_TYPE

The captcha protocol to use. Possible values are: `recaptchav3`

Example: `recaptchav3`

Default: An empty string (no captcha system will be used - not recommended)

Note: the relevant captcha field in the POST, e.g. `g-captcha-response`, will
be removed from the data that will be sent by email.

#### CAPTCHA_SECRET

The secret used to validate the request using a given secret.

Example: `d0n0tsh4r3m3`

Default: An empty string.

#### CAPTCHA_VERIFY_URL

The URL where challenge responses regarding the captcha can be verified, if
required.

Example: `https://www.google.com/recaptcha/api/siteverify`

Default: An empty string.

#### REDIRECT_URL

If set, redirect the client to the given URL. If not, set a 200 OK response
will be returned.

Example: `https://www.example.org/thank-you'

Default: An empty string

#### FIELDS_EXCLUDED

A list of fields in the POST request to exclude from the email. Fields are
comma separated. These fields take precedence over `FIELDS_INCLUDED`, i.e. if
a field is mentioned here it will be excluded even if it is listed in
`FIELDS_INCLUDED`.

Example: `secret_field1,secret_field2`

Default: An empty string (no fields are excluded)

#### FIELDS_INCLUDED

A list of fields in the POST request to include in the email. Fields are
comma separated. All other fields will be ignored, but only if they are not 
also mentioned in `FIELDS_EXCLUDED`

Example: `secret_field1,secret_field2`

Default: An empty string (no fields are excluded)

Note: captcha keys are automatically included.

#### ENABLE_DEBUG

Enable the debug resource. This provides various diagnostic information.

The resource will be made available at `DEBUG_PATH`

Default: `false`

Note: Only enable it when you're trying to debug a problem, 
since it will expose your  configuration variables and is expensive to render.

#### DEBUG_PATH

The path where the debug resource will be made available.

Default: `/debug`

