#!/usr/bin/env python
# coding: utf-8

import csv
import os
import base64
from passlib.hash import ldap_salted_sha1

# you can configure that
CSV_DELIMITER = ','
CSV_QUOTECHAR = '"'
ROLE_SEPARATOR = ';'
LDAP_ROOT_DN = 'dc=georchestra,dc=org'
EOL = '\n'
USERS_FILE = 'data/users.csv'
ORGS_FILE = 'data/orgs.csv'
HEADER = True

###  Nothing to edit past this line  ###

roles = {
    'SUPERUSER': {
        'id': 1,
        'users': [],
    },
    'ADMINISTRATOR': {
        'id': 2,
        'users': [],
    },
    'ORGADMIN': {
        'id': 3,
        'users': [],
    },
    'GN_ADMIN': {
        'id': 4,
        'users': [],
    },
    'GN_REVIEWER': {
        'id': 5,
        'users': [],
    },
    'GN_EDITOR': {
        'id': 6,
        'users': [],
    },
    'EXTRACTORAPP': {
        'id': 7,
        'users': [],
    },
    'USER': {
        'id': 8,
        'users': [],
    },
    'PENDING': {
        'id': 9,
        'users': [],
    }
}

orgs = {}

errors = []


def printOrgUnitDefinition():
    '''Print OU definitions'''
    users_def = ['# users, georchestra.org',
                 'dn: ou=users,' + LDAP_ROOT_DN,
                 'objectClass: organizationalUnit',
                 'objectClass: top',
                 'ou: users']
    print(EOL.join(users_def) + EOL)
    # print(EOL)

    roles_def = ['# roles, georchestra.org',
                 'dn: ou=roles,' + LDAP_ROOT_DN,
                 'objectClass: organizationalUnit',
                 'objectClass: top',
                 'ou: roles']
    print(EOL.join(roles_def) + EOL)

    orgs_def = ['# orgs, georchestra.org',
                'dn: ou=orgs,' + LDAP_ROOT_DN,
                'objectClass: organizationalUnit',
                'objectClass: top',
                'ou: orgs']
    print(EOL.join(orgs_def) + EOL)


def getField(rownb, value, fieldname):
    if value is '':
        # raise Exception("Empty " + fieldname + " on row " + str(rownb))
        errors.append("Empty " + fieldname + " on row " + str(rownb))
    return value


def main(roles, orgs):
    currentRoleUid = len(roles) + 1
    currentOrgUid = len(orgs) + 1
    rownb = 0

    if os.path.isfile(USERS_FILE):
        inputUsersReader = csv.reader(
            open(USERS_FILE, 'r'), delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR)

        if HEADER:
            next(inputUsersReader)

        for row in inputUsersReader:
            employeeNumber = row[0].strip()  # user id
            uid = getField(rownb, row[1].strip(), 'uid')  # login
            userPassword = ldap_salted_sha1.encrypt(
                getField(rownb, row[2].strip(), 'userPassword'))  # password
            mail = getField(rownb, row[3].strip(), 'mail')  # email
            if not mail.strip():
                uid + '@empty.com'
            givenName = row[4].strip()  # first name
            sn = row[5].strip()  # second name
            if not sn.strip():
                sn = uid
            o = row[6].strip()  # org / company
            title = row[7].strip()  # job situation
            telephoneNumber = row[8].strip()  # phone number
            postalAddress = row[9].strip()  # address

            currentRoles = getField(rownb, row[11], 'roles').replace(
                ' ', '').split(ROLE_SEPARATOR)
            for currentRole in currentRoles:
                currentRole = currentRole.strip()
                if not currentRole in roles:
                    roles[currentRole] = {'users': [], 'id': currentRoleUid}
                    currentRoleUid += 1
                roles[currentRole]['users'].append(
                    "uid=" + uid + ",ou=users," + LDAP_ROOT_DN)

            currentOrg = getField(rownb, row[6].strip(), 'org')
            if not currentOrg in orgs:
                orgs[currentOrg] = {'users': [], 'id': currentOrgUid}
                currentOrgUid += 1
            orgs[currentOrg]['users'].append(
                "uid=" + uid + ",ou=users," + LDAP_ROOT_DN)

            user = [
                '# user, ' + uid,
                'dn: uid=' + uid + ',ou=users,' + LDAP_ROOT_DN,
                'objectClass: inetOrgPerson',
                'objectClass: organizationalPerson',
                'objectClass: person',
                'objectClass: shadowAccount',
                'objectClass: top',
                'uid: ' + uid,
                'userPassword: ' + userPassword,
                'sn: ' + sn,
                'cn: ' + givenName + ' ' + sn,
                'mail: ' + mail
            ]

            if employeeNumber.strip() is not '':
                user.append('employeeNumber: ' + employeeNumber)
            if givenName.strip() is not '':
                user.append('givenName: ' + givenName)
            if title.strip() is not '':
                user.append('title: ' + title)
            if telephoneNumber.strip() is not '':
                user.append('telephoneNumber: ' + telephoneNumber)
            if postalAddress.strip() is not '':
                user.append(
                    'postalAddress:: ' + base64.b64encode(postalAddress.encode('windows-1252')).decode('utf8'))
            print(EOL.join(user) + EOL)

            rownb += 1

    for roleName, roleValues in roles.items():
        if roleName:
            role = [
                '# role, ' + roleName,
                'dn: cn=' + roleName + ',ou=roles,' + LDAP_ROOT_DN,
                'objectClass: groupOfMembers',
                'objectClass: top',
                'cn: ' + roleName
            ]
            # print(roleValues['users'])
            for member in roleValues['users']:
                role.append('member: ' + member)
            print(EOL.join(role) + EOL)

    if os.path.isfile(ORGS_FILE):
        inputOrgsReader = csv.reader(
            open(ORGS_FILE, 'r'), delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR)

        if HEADER:
            next(inputOrgsReader)

        for row in inputOrgsReader:
            ou = getField(rownb, row[1].strip(), 'ou')  # ou (obj 2)
            o1 = ou.lower()  # o (obj 1)
            o2 = getField(rownb, row[2].strip(), 'o2')  # o (obj 2)
            businessCategory = row[3].strip()  # businessCategory (obj 1)
            postalAddress = row[4].strip()  # postalAddress (obj 1)
            description = row[5].strip()  # description (obj 1)
            registered = row[6].strip()  # businessCategory (obj 2)

            org1 = [
                '# org, organization, ' + o1,
                'dn: o=' + o1 + ', ou=orgs, ' + LDAP_ROOT_DN,
                'objectClass: organization',
                'objectClass: top',
                'o: ' + o1,
                'businessCategory: ' + businessCategory
            ]

            if postalAddress:
                org1.append('postalAddress:: ' + base64.b64encode(postalAddress.encode(
                    'windows-1252')).decode('utf8'))

            print(EOL.join(org1) + EOL)

            org2 = [
                '# org, groupOfMembers, ' + o1,
                'dn: cn=' + o1 + ', ou=orgs, ' + LDAP_ROOT_DN,
                'objectClass: groupOfMembers',
                'objectClass: top',
                'cn: ' + o1,
                'o: ' + o2,
                'ou: ' + ou,
                'seeAlso: o=' + o1 + ', ou=orgs, ' + LDAP_ROOT_DN
            ]
            if description:
                org2.append('description:: ' + base64.b64encode(description.encode(
                    'windows-1252')).decode('utf8'))
            if registered:
                org2.append('businessCategory: REGISTERED')

            for orgName, orgValues in orgs.items():
                if orgName.lower() == o1:
                    for member in orgValues['users']:
                        org2.append('member: ' + member)

            print(EOL.join(org2) + EOL)


printOrgUnitDefinition()
main(roles, orgs)
# print(errors)
