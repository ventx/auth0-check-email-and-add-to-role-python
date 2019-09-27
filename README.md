# auth0-check-email-and-add-to-role-python
Auth0 Python code to check if E-Mail exists in Auth0 and if yes, get user_id and add to Auth0 Role.


This little script just reads in a file with email addresses (file should be one email address per line), checks whether the email address is associated with an Auth0 user and then adds this user to a role (it gets role_id by a provided role name). 

It prints how many users got added successfully and how many were not found - the latter will be written to a file on disk. Another file will be created for all the user_ids found for the email addresses.


## Requirements

* Python 3.5
* pip3: [auth0-python](https://pypi.org/project/auth0-python/)


