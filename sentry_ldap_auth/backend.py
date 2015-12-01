from __future__ import absolute_import

from django_auth_ldap.backend import LDAPBackend
from django.conf import settings
from sentry.models import (
    Organization,
    OrganizationMember,
    OrganizationMemberType,
    UserOption,
)


class SentryLdapBackend(LDAPBackend):
    def get_or_create_user(self, username, ldap_user):
        model = super(SentryLdapBackend, self).get_or_create_user(username, ldap_user)
        if len(model) < 1:
            return model

        user = model[0]

        user.is_managed = True

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

        if getattr(settings, 'AUTH_LDAP_SENTRY_ORGANIZATION_MEMBER_TYPE', None):
            member_type = getattr(OrganizationMemberType, settings.AUTH_LDAP_SENTRY_ORGANIZATION_MEMBER_TYPE)
        else:
            member_type = OrganizationMemberType.MEMBER

        if getattr(settings, 'AUTH_LDAP_SENTRY_ORGANIZATION_GLOBAL_ACCESS', False):
            has_global_access = True
        else:
            has_global_access = False

        # Add the user to the organization with global access
        OrganizationMember.objects.create(
            organization=organizations[0],
            type=member_type,
            has_global_access=has_global_access,
            user=user,
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
