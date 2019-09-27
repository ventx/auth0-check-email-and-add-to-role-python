import sys
import os
import json

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

# Auth0 Domain, Client ID and Client Secret of Auth0 Tenant
auth0_domain = '<AUTH0 TENANT DOMAIN>'
non_interactive_client_id = '<CLIENT ID>'
non_interactive_client_secret = '<CLIENT SECRET>'

get_token = GetToken(auth0_domain)
token = get_token.client_credentials(non_interactive_client_id,
                                     non_interactive_client_secret, 'https://{}/api/v2/'.format(auth0_domain))
mgmt_api_token = token['access_token']

auth0 = Auth0(auth0_domain, mgmt_api_token)

# Our ProdOrgUnits file to read email from
# Must be one email per line
prodorgunits_emails_filepath = 'emailaddresses.txt'

# Where to write Auth0 user_ids to
prodorgunits_auth0_userids_filepath = 'useridsonly.txt'

# Where to write not found Auth0 users
prodorgunits_auth0_not_found_filepath = 'notfound.txt'

# Auth0 Role to assign users to
auth0_role_name = "<ROLE NAME>"

user_emails = []
uids = []
emails_uids_dict = {}
count_found = 0
count_notfound = 0

with open(prodorgunits_emails_filepath) as fp:
    for line in fp:
        user_emails.append(line.rstrip('\n'))

# Read email addresses and search Auth0 for user_id
# If not found, write E-Mail address to seperate notfound file
with open(prodorgunits_auth0_not_found_filepath, 'w') as file:
    for email in user_emails:
        currentuser = auth0.users.list(q="email:" + email, fields=["user_id"])
        useridlist = []
        useridlist.clear()
        useridlist = currentuser['users']
        print(useridlist)
        try:
            userid = useridlist[0]
            uid = userid.get('user_id')
            uids.append(uid)
            emails_uids_dict[email] = uid
            count_found += 1
        except IndexError:
            file.write(email + "\n")
            count_notfound += 1

print("\n\n|--- Auth0 user_ids FOUND: " + str(count_found))
print("|--- Auth0 user_ids NOT FOUND " + str(count_notfound) + "\n")
print("|--- Auth0 email <=> user_id  Mapping \n")

for key, value in emails_uids_dict.items():
    print("[E-Mail]: ".ljust(15) + key.ljust(40) + " => [user_id]: ".ljust(20) + value + "\n")

print("\n\n|--- Auth0 user_ids FOUND: " + str(count_found))
print("|--- Auth0 user_ids NOT FOUND " + str(count_notfound) + "\n")

# Get role_id for role name
roledict = auth0.roles.list(name_filter=auth0_role_name)
roleidlist = roledict['roles']
roleiddict = roleidlist[0]
roleid = roleiddict.get('id')

# Write found user_ids to file
with open(prodorgunits_auth0_userids_filepath, 'w') as file:
    for i in uids:
        file.write(i + "\n")
        auth0.roles.add_users(id=roleid, users=[i])
        print("Added user to Auth0: " + i)


auth0_users_added = auth0.roles.list_users(id=roleid, include_totals=True)

# Print total users in Role
userstotal = auth0_users_added['total']
print("\n\nTOTAL USERS ADDED: " + str(userstotal))
