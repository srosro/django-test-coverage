Django Test Coverage
====================

Overview
--------

The test runner is an extended version of the default django test runner. It adds the ability to get coverage reports from defined modules or tested apps.

.. _Coverage: http://nedbatchelder.com/code/modules/coverage.html

Usage
-----

Simple add the line

    TEST_RUNNER = 'django-test-coverage.runner.run_tests'

to your django settings file. If you run the test with

    python manage.py test zoo

the test runner will evaluate all modules in the app *zoo* and add them to the coverage report. You can also specify a set of modules by adding the line

    COVERAGE_MODULES = ('zoo.baer', 'zoo.lion')

to your settings file. In this example *zoo* should be replaced with your application name and *baer/lion* with your module included in the reported.

Limitations
-----------

So far no implementation to wrap around djangos PostGIS test runner.