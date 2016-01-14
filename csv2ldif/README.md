As its name suggests, the [CSV2LDIF python script](./CSV2LDIF.py) allows one to create a LDIF file from a CSV.

Pre-Requisites
==============

Python should be installed and passlib available

The CSV file is expected:
 * to be in the same folder as the script
 * to be called users.csv
 * to use commas as separators
 * to have quotes (double) around fields
 * to expose LDAP user fields in this order: employeeNumber, uid, userPassword, mail, givenName, sn, o, title, telephoneNumber, groups

Note that:
 * uid, userPassword, mail & groups fields are mandatory, the others can be left blank (but not skipped).
 * group names should be separated by semicolons


Usage
=====

    python CSV2LDIF.py > my.ldif

Note that the LDIF file will be generated for the dc=georchestra,dc=org root dn.
To change this, feel free to edit the script.

The generated LDIF file is meant to be inserted in the LDAP right after the georchestra-bootstrap.ldif file, as it creates the full tree, including the root dn.