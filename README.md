# sentry-ldap-auth

A Django custom authentication backend for [Sentry](https://github.com/getsentry/sentry). This module extends the functionality of [django-auth-ldap](https://pythonhosted.org/django-auth-ldap/) with Sentry specific features.

## Features
* Users created by this backend are managed users. Managed fields are not editable through the Sentry account page.
* Users may be auto-added to an Organization upon creation.

## Prerequisites
Versions 2.0 and newer require Sentry 8. For Sentry 7 support, use [the 1.1 release](https://github.com/Banno/getsentry-ldap-auth/releases/tag/1.1)

## Configuration
This module extends the [django-auth-ldap](https://pythonhosted.org/django-auth-ldap/) and all the options it provides are supported.

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
AUTH_LDAP_SENTRY_ORGANIZATION_GLOBAL_ACCESS = True

AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + (
    'sentry_ldap_auth.backend.SentryLdapBackend',
)

import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel('DEBUG')
```
