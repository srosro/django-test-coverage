Django Test Coverage
====================

Overview
--------

The test runner is an extended version of the default django test runner. It adds the ability to get coverage reports from defined modules or tested apps.

.. _Coverage: http://nedbatchelder.com/code/modules/coverage.html

Update(11-20-13)
------

This version(0.2.5) supports python 3.3.x and django 1.6

Usage
-----

Simple add the line

    Add 'django_test_runner' to INSTALLED_APPS

	Django 1.3 and earlier:
	TEST_RUNNER = 'django_test_coverage.runner.run_tests'

	Django 1.4 to 1.6:
	TEST_RUNNER = 'django_test_coverage.runner.CoverageTestSuiteRunner'


to your django settings file. If you run the test with

    python manage.py test zoo

the test runner will evaluate all modules in the app *zoo* and add them to the coverage report. You can also specify a set of modules by adding the line

    COVERAGE_MODULES = ('zoo.baer', 'zoo.lion')

to your settings file. In this example *zoo* should be replaced with your application name and *baer/lion* with your module included in the reported.  Modules can be ignored with

    COVERAGE_EXCLUDE_MODULES = ('zoo.tests',)

This will exclude *zoo.tests* and all its submodules from the coverage statistics.

You can also specify a set of apps to test. This option performs in a similar manner to specifying specific apps on the command line, but here you can specify a default set of apps to test in the settings file. To specify a set of apps, add the line

	COVERAGE_APPS = ('zoo',)

to your settings file. In this example, the test runner will evaluate all modules in the app *zoo* and add them to the coverage report whenever you run the following line

	python manage.py test

Any apps specified at the command line will override the COVERAGE_MODULES and COVERAGE_APPS options.

Reporters
---------

In addition to the default console reporter, you can specify either 'html' or 'xml' as the value of COVERAGE_REPORT_TYPE.

The HTML reporter has the following options:

    COVERAGE_HTML_DIRECTORY: Directory to output html to; defaults to covhtml in the current directory. If the directory doesn't exist it'll be created.
    COVERAGE_HTML_EXTRA_CSS: An extra css file that coverage'll copy into the output directory if given; defaults to None.
    COVERAGE_HTML_OPEN_IN_BROWSER: Whether or not to open the index file after generation. Uses the webbrowser module to do so. Default is False.
    COVERAGE_HTML_BROWSER_OPEN_TYPE: If COVERAGE_HTML_OPEN_IN_BROWSER is True, then this dictates how the open is done.  Possible values are 'existing' (use existing browser window), 'new' (try and open a new browser), or 'tab' (python >= 2.5 only; attempts to open in a new tab). See http://docs.python.org/library/webbrowser.html#webbrowser.open for details.

The XML reporter has the following options:

    COVERAGE_XML_FILE: Specifies the output path or outputs to coverage.xml if not specified.

Limitations
-----------

So far no implementation to wrap around djangos PostGIS test runner.
