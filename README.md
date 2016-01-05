# Introduction
The akonadi-initalisync tool can be used to setup a users account initally and synchronize it in a scripted fashion.
This is useful for preparing workstations so they are ready once the user logs in.

The script takes some parameters to adjust the per user settings, and reads the rest of the configuration from configuration-file templates.

After preparing the necessary configuration files, the script automatically starts dbus and akonadi, executes the sync, and then shuts akonadi and dbus down again.
The script is fully blocking during this time, so it can easly be included in other scripts.

Please note that the script accesses the users home directory (where the configuration files reside), and thus needs to be run as the respective user.

# Requirements
The script needs to be running as the target user, and all necessary packages need to be installed.
The script allso needs to be executed using ipython at requires access to an X11 session.

Required packages:

* ipython
* acl
* dbus-x11
* kontact
* kwalletcli
* libicu48
* python-gobject
* python-dbus

# Usage
The script is used as follows:
```
ipython initalsync.py "$NAME" "$MAIL" "$UID" "$PASSWORD" "akonadi_kolab_resource_0"
```

* NAME: The name of the user. Used for identity configuration.
* MAIL: The email-address of the user. Used for identity configuration and as login for the kolab server.
* UID: The uid of the user. Used for access to the kolab user and as database- and user-name in the MYSQL database (by default). Used as the "{uid}" template parameter.
* PASSWORD: Used as password to access the MYSQL database as well as access to the kolab server. Used as the "{password}" template parameter.

An example use could look like this:
```
ipython initalsync.py "John Doe" "doe@example.com" "doe" "MyPass1234" "akonadi_kolab_resource_0"
```

The test.sh script demonstrates usage using a local MYSQL server.

# Templates
Most configuration options can be adjusted by adjusting the templates in "sync/templates/".

The akonadi MYSQL settings are located in:
```
sync/templates/.config/akonadi/akonadiserverrc
```

The kolab server settings are located in:
```
sync/templates/.kde/share/config/akonadi_kolab_resource_0rc
```

The ldap server settings are located in:
```
sync/templates/.kde/share/config/akonadi_ldap_resource_0rc
sync/templates/.kde/share/config/kabldaprc
```
