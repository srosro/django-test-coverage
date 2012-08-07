from setuptools import setup, find_packages

VERSION = '0.2'

DESCRIPTION = '''

Django Test Coverage
====================

Overview
--------

The test runner is an extended version of the default Django test runner. It
adds the ability to get coverage reports from defined modules or tested apps.

It requires Ned Batchelder's coverage.py: http://nedbatchelder.com/code/modules/coverage.html

Usage
-----

Simple add the line

    TEST_RUNNER = 'django_test_coverage.runner.run_tests'

to your Django settings file. If you run the test with

    python manage.py test foo

the test runner will evaluate all modules in the app *foo* and add them to the
coverage report. You can also specify a set of modules by adding the line

    COVERAGE_MODULES = ('foo.bar', 'foo.baz')

to your settings file. In this example *foo* should be replaced with your
application name and *bar/baz* with your module included in the reported.

Limitations
-----------

There is no implementation to wrap around Django's PostGIS test runner.


Changelog
=========

0.1 (2009-03-03)
----------------

- Initial Release

0.2 (2012-08-07)
----------------

- New maintainer
- Added Django 1.4 compatibility
- Added support for specifying a default set of apps to perform coverage on
- Misc bugfixes & cleanup

'''

setup(
    name='django-test-coverage',
    version=VERSION,
    author='stj',
    author_email='stefan (at) tjarks (dot) de',
    #maintainer='srosro',
    #maintainer_email='sam (at) odio (dot) com',
    description='A simple way to get your Django application\'s test coverage.',
    long_description=DESCRIPTION,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
    keywords='django,test,coverage',
    url='http://github.com/srosro/django-test-coverage',
    license='MIT',
    packages=['django_test_coverage'],
    requires=['coverage'],
    include_package_data=True,
    zip_safe=False,
    platforms=['linux', 'unix', 'windows', 'mac'],
    download_url='https://github.com/srosro/django-test-coverage/zipball/master',
)

