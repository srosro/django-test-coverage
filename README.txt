Django Test Coverage
====================

Overview
--------

The test runner is an extended version of the default django test runner. It adds the ability to get coverage reports from defined modules or tested apps.

.. _Coverage: http://nedbatchelder.com/code/modules/coverage.html

Usage
-----

Simple add the line
	
	Django 1.3 and earlier:
	TEST_RUNNER = 'django-test-coverage.runner.run_tests'
	
	Django 1.4:
	TEST_RUNNER = 'django_test_coverage.runner.CoverageTestSuiteRunner'
	

to your django settings file. If you run the test with

    python manage.py test zoo

the test runner will evaluate all modules in the app *zoo* and add them to the coverage report. You can also specify a set of modules by adding the line

    COVERAGE_MODULES = ('zoo.baer', 'zoo.lion')

to your settings file. In this example *zoo* should be replaced with your application name and *baer/lion* with your module included in the reported.

You can also specify a set of apps to test. This option performs in a similar manner to specifying specific apps on the command line, but here you can specify a default set of apps to test in the settings file. To specify a set of apps, add the line

	COVERAGE_APPS = ('zoo',)

to your settings file. In this example, the test runner will evaluate all modules in the app *zoo* and add them to the coverage report whenever you run the following line

	python manage.py test

Any apps specified at the command line will override the COVERAGE_MODULES and COVERAGE_APPS options.

Limitations
-----------

So far no implementation to wrap around djangos PostGIS test runner.