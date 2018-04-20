from __future__ import absolute_import

from django_auth_ldap.backend import LDAPBackend
from django.conf import settings
from django.db.models import Q
from sentry.models import (
    Organization,
    OrganizationMember,
    UserOption,
)


class SentryLdapBackend(LDAPBackend):
    def get_or_create_user(self, username, ldap_user):
        username_field = getattr(settings, 'AUTH_LDAP_SENTRY_USERNAME_FIELD', '')
        if username_field:
            # pull the username out of the ldap_user info
            if ldap_user and username_field in ldap_user.attrs:
                username = ldap_user.attrs[username_field]
                if isinstance(username, (list, tuple)):
                    username = username[0]

        model = super(SentryLdapBackend, self).get_or_create_user(username, ldap_user)
        if len(model) < 1:
            return model

        user = model[0]

        user.is_managed = True

        # Add the user email address
        try:
            from sentry.models import (UserEmail)
        except ImportError:
            pass
        else:
            if 'mail' in ldap_user.attrs:
                email = ldap_user.attrs.get('mail')[0]
            elif not hasattr(settings, 'AUTH_LDAP_DEFAULT_EMAIL_DOMAIN'):
                email = ''
            else:
                email = username + '@' + settings.AUTH_LDAP_DEFAULT_EMAIL_DOMAIN

            # django-auth-ldap may have accidentally created an empty email address
            UserEmail.objects.filter(Q(email='') | Q(email=' '), user=user).delete()
            if email:
                UserEmail.objects.get_or_create(user=user, email=email)

        # Check to see if we need to add the user to an organization
        if not settings.AUTH_LDAP_DEFAULT_SENTRY_ORGANIZATION:
            return model

        # If the user is already a member of an organization, leave them be
        orgs = OrganizationMember.objects.filter(user=user)
        if orgs != None and len(orgs) > 0:
            return model

        # Find the default organization
        organizations = Organization.objects.filter(name=settings.AUTH_LDAP_DEFAULT_SENTRY_ORGANIZATION)

        if not organizations or len(organizations) < 1:
            return model

        member_role = getattr(settings, 'AUTH_LDAP_SENTRY_ORGANIZATION_ROLE_TYPE', 'member')
        has_global_access = getattr(settings, 'AUTH_LDAP_SENTRY_ORGANIZATION_GLOBAL_ACCESS', False)

        # Add the user to the organization with global access
        OrganizationMember.objects.create(
            organization=organizations[0],
            user=user,
            role=member_role,
            has_global_access=has_global_access,
            flags=getattr(OrganizationMember.flags, 'sso:linked'),
        )

        if not getattr(settings, 'AUTH_LDAP_SENTRY_SUBSCRIBE_BY_DEFAULT', True):
            UserOption.objects.set_value(
                user=user,
                project=None,
                key='subscribe_by_default',
                value='0',
            )

        return model
