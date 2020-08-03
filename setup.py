#!/usr/bin/env python
"""
sentry-ldap-auth
==============

An extension for Sentry which authenticates users from
an LDAP server and auto-adds them to the an organization in sentry.
"""
from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

install_requires = [
    'django-auth-ldap==1.7.*',  # Last version to support Python 2.7
    'sentry>=10.0.0',
]

setup(
    name='sentry-ldap-auth',
    version='2.8.1',
    author='Chad Killingsworth <chad.killingsworth@banno.com>, Barron Hagerman <barron.hagerman@banno.com>',
    author_email='chad.killingsworth@banno.com',
    url='http://github.com/banno/getsentry-ldap-auth',
    description='A Sentry extension to add an LDAP server as an authentication source.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    license='Apache-2.0',
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    download_url='https://github.com/banno/getsentry-ldap-auth/tarball/2.8.1',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
