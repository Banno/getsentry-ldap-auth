# sentry-ldap-auth

A Django custom authentication backend for [Sentry](https://github.com/getsentry/sentry). This module extends the functionality of [django-auth-ldap](https://pythonhosted.org/django-auth-ldap/) with Sentry specific features.

## Features
* Users created by this backend are managed users. Managed fields are not editable through the Sentry account page.
* Users may be auto-added to an Organization upon creation.

## Configuration
This module extends the [django-auth-ldap](https://pythonhosted.org/django-auth-ldap/) and all the options it provides are supported.

### sentry-ldap-auth Specific Options

```Python
AUTH_LDAP_DEFAULT_SENTRY_ORGANIZATION = u'My Organization Name'
```
Auto adds created user to the specified organization (matched by name) if it exists.

```Python
AUTH_LDAP_SENTRY_ORGANIZATION_MEMBER_TYPE = 'MEMBER'
```
Member type auto-added users are assigned. Valid values are 'MEMBER', 'ADMIN', 'OWNER'.

```Python
AUTH_LDAP_SENTRY_ORGANIZATION_GLOBAL_ACCESS = True
```
Whether auto-created users should be granted global access within the default organization.

### Sentry Options

```Python
SENTRY_MANAGED_USER_FIELDS = ('email', 'first_name', 'last_name', 'password', )
```

Fields which managed users may not modify through the Sentry accounts view. Applies to all managed accounts.
