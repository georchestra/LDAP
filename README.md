This directory contains 3 LDIF files which aim to facilitate LDAP configuration.

There are 2 main ways of having openLDAP configured :

- One using a single conf file (on debian/ubuntu systems, located in
  /etc/ldap/sldapd.conf)

- A new one which tends to store the configuration into a specific LDAP branch
  (name cn=config), and composed of several files located generally into
  /etc/ldap/slapd.d).

We document here the second case (slapd.d-style configuration).


The file **georchestra-bootstrap.ldif** allows to create the db entry.
It should mainly be used this way:

    $ sudo ldapadd -Y EXTERNAL -H ldapi:/// -f georchestra-bootstrap.ldif


If everything was successful with the previous command, you now have to create
the root DN. Note that the previous command should have set the default
administrator account as:

    dn: cn=admin,dc=georchestra,dc=org
    password: secret

You can then issue the following command in order to create the root DN with **georchestra-root.ldif**:

    $ ldapadd -D"cn=admin,dc=georchestra,dc=org" -W -f georchestra-root.ldif 

The **georchestra.ldif** file allows one to create the default geOrchestra users & groups:

    $ ldapadd -D"cn=admin,dc=georchestra,dc=org" -W -f georchestra.ldif 

Note that you are free to customize the users (entries under the "users" OrganizationUnit) to fit your needs, provided you keep the required extractorapp_privileged_admin.
For the testuser, testreviewer, testeditor and testadmin users, passwords are identical to login.



Another file is provided but it is optional: **gidnumber-uniqueness.ldif**. 
It aims to add a unicity constraint on each objects under the base
ou=groups,dc=georchestra,dc=org, so that another group is added, it should have
a unique gidNumber attribute.

