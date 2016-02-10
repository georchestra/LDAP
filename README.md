# LDAP

This repository contains several optional utilities related to OpenLDAP for the [geOrchestra](http://www.georchestra.org) SDI:
 * a [CSV2LDIF](csv2ldif/README.md) python script which allows one to create a LDIF file from a CSV
 * a smallish [java LDAP service](embedded-ldap/README.md) for testing purposes
 * a [script to add unique identifiers](geofence-uniqueids/add-unique-ids.py) on each user and group of an existing LDAP tree, which can be used to upgrade an existing ldap tree for use with geofence
