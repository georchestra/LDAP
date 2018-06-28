As its name suggests, the [CSV2LDIF python script](./CSV2LDIF.py) allows one to create a LDIF file from a CSV.

# Pre-Requisites

Python should be installed and passlib available

2 CSV files are required:

- the users file whose path is defined as "USERS_FILE" variable
- the orgs file whose path is defined as "ORGS_FILE" variable

The CSV files are expected:

- to be defined in "USERS_FILE" and "ORGS_FILE" variables
- to use commas as separators
- to have quotes (double) around fields
- to expose LDAP user fields in this order: employeeNumber, uid, userPassword, mail, givenName, sn, o, title, telephoneNumber, postalAddress, groups (cf. fields name in users.csv)
- to expose LDAP orgs fields in this order: id, ou (short name), o (name), businessCategory, postalAddress, description, registered (cf. fields name in orgs.csv)

Note that:

- uid, userPassword, mail & groups fields are mandatory, the others can be left blank (but not skipped).
- roles names should be separated by semicolons

# Usage

    python CSV2LDIF.py > my.ldif

This script has been tested with Python 3.6.
It need the "base64" module to work.

Note that the LDIF file will be generated for the dc=georchestra,dc=org root dn.
To change this, feel free to edit the script.

The generated LDIF file is meant to be inserted in the LDAP right after the georchestra-bootstrap.ldif file, as it creates the full tree, including the root dn.
