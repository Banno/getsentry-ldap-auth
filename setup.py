#!/usr/bin/env python
"""
sentry-banno-auth
==============

An extension for Sentry which authenticates users from
Banno LDAP servers and auto-adds them to the Banno organization in sentry.
"""
from setuptools import setup, find_packages

install_requires = [
    'django-auth-ldap>=1.2.5',
    'sentry>=7.4.0',
]

setup(
    name='sentry-ldap-auth',
    version='1.0',
    author='Chad Killingsworth - Jack Henry and Associates, Inc.',
    author_email='chad.killingsworth@banno.com',
    url='http://github.com/banno/getsentry-ldap-auth',
    description='A Sentry extension to add an LDAP server as an authention source.',
    long_description=__doc__,
    packages=find_packages(),
    license='Apache-2.0',
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
