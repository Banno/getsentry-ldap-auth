#!/usr/bin/env python
"""
sentry-ldap-auth
==============

An extension for Sentry which authenticates users from
an LDAP server and auto-adds them to the an organization in sentry.
"""
from setuptools import setup, find_packages

install_requires = [
    'django-auth-ldap>=1.2.5',
    'sentry>=8.0.0',
]

setup(
    name='sentry-ldap-auth',
    version='2.3',
    author='Chad Killingsworth <chad.killingsworth@banno.com>, Barron Hagerman <barron.hagerman@banno.com>',
    author_email='chad.killingsworth@banno.com',
    url='http://github.com/banno/getsentry-ldap-auth',
    description='A Sentry extension to add an LDAP server as an authention source.',
    long_description=__doc__,
    packages=find_packages(),
    license='Apache-2.0',
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    download_url='https://github.com/banno/getsentry-ldap-auth/tarball/1.1',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
