# sentry-ldap-auth

A Django custom authentication backend for [Sentry](https://github.com/getsentry/sentry). This module extends the functionality of [django-auth-ldap](https://github.com/django-auth-ldap/django-auth-ldap) with Sentry specific features.

## Features
* Users created by this backend are managed users. Managed fields are not editable through the Sentry account page.
* Users may be auto-added to an Organization upon creation.

## Prerequisites
Versions 2.0 and newer require Sentry 8. For Sentry 7 support, use [the 1.1 release](https://github.com/Banno/getsentry-ldap-auth/releases/tag/1.1)

## Installation
To install, simply add `sentry-ldap-auth` to your *requirements.txt* in your Sentry environment 
and install gcc in your *Dockerfile* in the same config 
```shell script
RUN apt-get update && apt-get install -y gcc
```
## Configuration
This module extends the [django-auth-ldap](https://django-auth-ldap.readthedocs.io/en/latest/) and almost all the options are supported (up until 1.7.*)
One options that's not supported is `AUTH_LDAP_MIRROR_GROUPS` .

To configure Sentry to use this module, add `sentry_ldap_auth.backend.SentryLdapBackend` to your `AUTHENTICATION_BACKENDS` in your *sentry.conf.py*, like this:

```python
AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + (
    'sentry_ldap_auth.backend.SentryLdapBackend',
)
```

Then, add any applicable configuration options. Depending on your environment, and especially if you are running Sentry in containers, you might consider using [python-decouple](https://pypi.python.org/pypi/python-decouple) so you can set these options via environment variables.

### sentry-ldap-auth Specific Options

```Python
AUTH_LDAP_DEFAULT_SENTRY_ORGANIZATION = u'My Organization Name'
```
Auto adds created user to the specified organization (matched by name) if it exists.

```Python
AUTH_LDAP_SENTRY_ORGANIZATION_ROLE_TYPE = 'member'
```
Role type auto-added users are assigned. Valid values in a default installation of Sentry are 'member', 'admin', 'manager' & 'owner'. However, custom roles can also be added to Sentry, in which case these are also valid.

```Python
AUTH_LDAP_SENTRY_ORGANIZATION_GLOBAL_ACCESS = True
```
Whether auto-created users should be granted global access within the default organization.
 
```Python
AUTH_LDAP_SENTRY_SUBSCRIBE_BY_DEFAULT = False
```
Whether new users should be subscribed to any new projects by default. Disabling
this is useful for large organizations where a subscription to each project
might be spammy.

```Python
AUTH_LDAP_SENTRY_USERNAME_FIELD = 'uid'
```
Specify which attribute to use as the Sentry username, if different from what the user enters on the login page. You can use this to prevent multiple accounts from being created when your `AUTH_LDAP_USER_SEARCH` allows users to log in with different usernames (e.g. `(|(uid=%(user))(mail=%(user)))`). If multiple values exist for the attribute, the first value will be used.

```Python
AUTH_LDAP_DEFAULT_EMAIL_DOMAIN = 'example.com'
```
Default domain to append to username as the Sentry user's e-mail address when the LDAP user has no `mail` attribute.
 
### Sentry Options

```Python
SENTRY_MANAGED_USER_FIELDS = ('email', 'first_name', 'last_name', 'password', )
```

Fields which managed users may not modify through the Sentry accounts view. Applies to all managed accounts.

### Example Configuration

```Python
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfUniqueNamesType

AUTH_LDAP_SERVER_URI = 'ldap://my.ldapserver.com'
AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''

AUTH_LDAP_USER_SEARCH = LDAPSearch(
    'dc=domain,dc=com',
    ldap.SCOPE_SUBTREE,
    '(mail=%(user)s)',
)

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    '',
    ldap.SCOPE_SUBTREE,
    '(objectClass=groupOfUniqueNames)'
)

AUTH_LDAP_GROUP_TYPE = GroupOfUniqueNamesType()
AUTH_LDAP_REQUIRE_GROUP = None
AUTH_LDAP_DENY_GROUP = None

AUTH_LDAP_USER_ATTR_MAP = {
    'name': 'cn',
    'email': 'mail'
}

AUTH_LDAP_FIND_GROUP_PERMS = False
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

AUTH_LDAP_DEFAULT_SENTRY_ORGANIZATION = u'My Organization Name'
AUTH_LDAP_SENTRY_ORGANIZATION_ROLE_TYPE = 'member'
AUTH_LDAP_SENTRY_GROUP_ROLE_MAPPING = {
    'owner': ['sysadmins'],
    'admin': ['devleads'],
    'member': ['developers', 'seniordevelopers']
}
AUTH_LDAP_SENTRY_ORGANIZATION_GLOBAL_ACCESS = True
AUTH_LDAP_SENTRY_USERNAME_FIELD = 'uid'

AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + (
    'sentry_ldap_auth.backend.SentryLdapBackend',
)

import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel('DEBUG')
```
