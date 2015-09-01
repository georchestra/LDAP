#!/usr/bin/python
import ldap
import ldap.modlist
import string
import sys
import base64

# This sample script allows to add an unique identifier attribute
# on each user and group of an existing LDAP tree.

# it is recommended to load the unique OpenLDAP overlay before using this
# script. See:
# http://www.openldap.org/doc/admin24/overlays.html#Attribute Uniqueness

STR_RED   = "\033[01;31m{0}\033[00m"
STR_GREEN = "\033[1;36m{0}\033[00m"

# OpenLDAP
LDAP_URI    = 'ldap://localhost:389'
LDAP_BINDDN = 'cn=admin,dc=georchestra,dc=org'
LDAP_PASSWD = 'secret'

USERS_OBJ_CLASS='inetOrgPerson'
USERS_UID_ATTRIBUTE='employeeNumber'
USERS_LDAP_FILTER='(&(objectClass=%s)(!(%s=*)))' % (USERS_OBJ_CLASS,USERS_UID_ATTRIBUTE,)
USERS_LDAP_BASEDN='ou=users,dc=georchestra,dc=org'

GROUPS_OBJ_CLASS='groupOfMembers'
GROUPS_UID_ATTRIBUTE='ou'
GROUPS_LDAP_FILTER='(&(objectClass=%s)(!(%s=*)))' % (GROUPS_OBJ_CLASS, GROUPS_UID_ATTRIBUTE,)
GROUPS_LDAP_BASEDN='ou=groups,dc=georchestra,dc=org'

current_userid  = 0
current_groupid = 0
# Connection to the LDAP server

ldapCnx = ldap.initialize(LDAP_URI)
ldapCnx.simple_bind_s(LDAP_BINDDN, LDAP_PASSWD)
ldapCnx.protocol_version = ldap.VERSION3

# Adds a employeeNumber to the user
def openldap_add_uid_to_user(user_dn, number, dry_run):
  mod_attrs = [(ldap.MOD_ADD, USERS_UID_ATTRIBUTE, str(number))]
  if not dry_run:
    try:
      ldapCnx.modify_s(user_dn, mod_attrs)
    except ldap.CONSTRAINT_VIOLATION:
      return openldap_add_uid_to_user(user_dn, number + 1, dry_run)
    except ldap.LDAPError, e:
      print STR_RED.format("[Error]: %s" % e)
      return False
  else:
    print STR_GREEN.format("[dry-run] Assigning uid %s to user %s\n" % (number, user_dn,))
  return True

# Checks if a group already owns the identifier
def gid_exists(gid):
  ldap_result_id = ldapCnx.search(GROUPS_LDAP_BASEDN, ldap.SCOPE_ONELEVEL,"(%s=%d)" % (GROUPS_UID_ATTRIBUTE, gid,), None, 1)
  _ , result_data = ldapCnx.result(ldap_result_id, 0)
  if (result_data == []):
    return False
  else:
    return True

# Adds a unique identifier to the group
def openldap_add_uid_to_group(group_dn, number, dry_run):
  mod_attrs = [(ldap.MOD_ADD, GROUPS_UID_ATTRIBUTE, str(number))]
  if not dry_run:
    try:
      ldapCnx.modify_s(group_dn, mod_attrs)
    except ldap.LDAPError, e:
      print STR_RED.format("[Error]: %s" % e)
      return False
  else:
    print STR_GREEN.format("[dry-run] Assigning uid %s to group %s\n" % (number, group_dn,))
  return True

# Actually do something
if __name__ == "__main__":
  users  = []
  # getting users from the LDAP
  try:
    ldap_result_id = ldapCnx.search(USERS_LDAP_BASEDN, ldap.SCOPE_ONELEVEL, USERS_LDAP_FILTER, None, 1)
    while 1:
      result_type, result_data = ldapCnx.result(ldap_result_id, 0)
      if (result_data == []):
        break
      else:
        if result_type == ldap.RES_SEARCH_ENTRY:
          users.append(result_data)
  except ldap.LDAPError, e:
    print STR_RED.format(e)
  groups = []
  # getting groups from the LDAP
  try:
    ldap_result_id = ldapCnx.search(GROUPS_LDAP_BASEDN, ldap.SCOPE_ONELEVEL, GROUPS_LDAP_FILTER, None, 1)
    while 1:
      result_type, result_data = ldapCnx.result(ldap_result_id, 0)
      if (result_data == []):
        break
      else:
        if result_type == ldap.RES_SEARCH_ENTRY:
          groups.append(result_data)
  except ldap.LDAPError, e:
    print STR_RED.format(e)

  # Adds a unique identifier on the users
  for usr in users:
    dn, _ = usr[0]
    print STR_GREEN.format(dn)
    openldap_add_uid_to_user(dn, current_userid, False)
    current_userid += 1

  # Adds a unique identifier on the groups
  for group in groups:
    dn, _ = group[0]
    print STR_GREEN.format(dn)
    while (gid_exists(current_groupid)):
      current_groupid += 1
    openldap_add_uid_to_group(dn, current_groupid, False)
    current_groupid += 1

  # end: disconnect
  ldapCnx.unbind_s()

