#!/usr/bin/env python
import csv
from passlib.hash import ldap_md5_crypt

# you can configure that
CSV_DELIMITER = ','
CSV_QUOTECHAR = ''
GROUP_SEPARATOR = ';'
LDAP_ROOT_DN = 'dc=georchestra,dc=org'
EOL = "\r\n"

###  Nothing to edit past this line  ###

print """dn: """+LDAP_ROOT_DN+"""
objectClass: top
objectClass: dcObject
objectclass: organization
o: geOrchestra LDAP
dc: georchestra
description: geOrchestra LDAP tree
"""

print """dn: ou=groups,"""+LDAP_ROOT_DN+"""
objectClass: organizationalUnit
objectClass: top
ou: groups
description: geOrchestra groups
"""

print """dn: ou=users,"""+LDAP_ROOT_DN+"""
objectClass: organizationalUnit
objectClass: top
ou: users
description: geOrchestra users
"""

inputReader = csv.reader(open('users.csv', 'rb'), delimiter=CSV_DELIMITER)

groups = {
    'ADMINISTRATOR': {
        'id': 1,
        'users': [],
    },
    'SV_ADMIN': {
        'id': 2,
        'users': [],
    },
    'SV_ADMIN_USERS': {
        'id': 3,
        'users': [],
    },
    'STAT_USER': {
        'id': 4,
        'users': [],
    },
    'SV_EDITOR': {
        'id': 5,
        'users': [],
    },
    'SV_REVIEWER': {
        'id': 6,
        'users': [],
    },
    'SV_USER': {
        'id': 7,
        'users': [],
    },
}

currentUid = 10

for row in inputReader:
    employeeNumber   = row[0] # user id
    uid              = row[1] # login
    userPassword     = ldap_md5_crypt.encrypt(row[2]) # don't save cleartext passwords
    mail             = row[3] # email
    givenName        = row[4] # first name
    sn               = row[5] # second name
    o                = row[6] # org / company
    title            = row[7] # job situation
    telephoneNumber  = row[8] # phone number
    currentGroups    = row[9].replace(' ', '').split(GROUP_SEPARATOR)

    for currentGroup in currentGroups:
        if not groups.has_key(currentGroup):
            groups[currentGroup] = {'users': [], 'id': currentUid}
            currentUid += 1
        groups[currentGroup]['users'].append(uid)

    print "dn: uid="+uid+",ou=users," + LDAP_ROOT_DN + EOL,
    print "objectClass: inetOrgPerson" + EOL,
    print "objectClass: organizationalPerson" + EOL,
    print "objectClass: person" + EOL,
    print "objectClass: top" + EOL,
    print "uid: "              + uid + EOL,
    print "employeeNumber: "   + employeeNumber + EOL,
    print "sn: "               + sn + EOL,
    print "givenName: "        + givenName + EOL,
    print "o: "                + o + EOL,
    if title is not '':
        print "title: "        + title + EOL,
    print "cn: "               + givenName + " " + sn + EOL,
    print "userPassword: "     + userPassword + EOL,
    print "mail: "             + mail + EOL,
    print "telephoneNumber: "  + telephoneNumber + EOL


for groupName,o in groups.items():
    print "dn: cn=" + groupName + ",ou=groups," + LDAP_ROOT_DN + EOL,
    print "objectClass: posixGroup" + EOL,
    print "objectClass: top" + EOL,
    print "cn: " + groupName + EOL,
    for memberUid in o['users']:
        print "memberUid: uid=" + memberUid + ",ou=users," + LDAP_ROOT_DN + EOL,
    print "gidNumber: " + str(o['id']) + EOL
