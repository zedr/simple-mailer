# Simple Mailer
A simple Python mailer script that's suitable for Namecheap Shared Hosting.

[![Build Status](https://travis-ci.com/zedr/simple-mailer.svg?branch=master)](https://travis-ci.com/zedr/simple-mailer)

## Installation

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

The captcha protocol to use. Possible values are: `recaptchav3`

Example: `recaptchav3`

Default: An empty string (no captcha system will be used - not recommended)

Note: the relevant captcha field in the POST, e.g. `g-captcha-response`, will
be removed from the data that will be sent by email.

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
comma separated. These fields take precedence over `FIELDS_INCLUDED`, i.e. if
a field is mentioned here it will be excluded even if it is listed in
`FIELDS_INCLUDED`.

Example: `secret_field1,secret_field2`

Default: An empty string (no fields are excluded)

### FIELDS_INCLUDED

A list of fields in the POST request to include in the email. Fields are
comma separated. All other fields will be ignored, but only if they are not 
also mentioned in `FIELDS_EXCLUDED`

Example: `secret_field1,secret_field2`

Default: An empty string (no fields are excluded)

Note: don't forget to add your captcha fields if you set this variable!

