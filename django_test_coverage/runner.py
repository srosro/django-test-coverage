# -*- coding: utf-8 -*-
import os

from django.db.models import get_app
from django.conf import settings

import coverage

def run_tests(test_labels, verbosity=1, interactive=True, failfast=False, extra_tests=[]):
    """
    Run the unit tests for all the test labels in the provided list.
    Labels must be of the form:
     - app.TestClass.test_method
        Run a single specific test method
     - app.TestClass
        Run all the test methods in a given class
     - app
        Search for doctests and unittests in the named application.

    When looking for tests, the test runner will look in the models and
    tests modules for the application.

    A list of 'extra' tests may also be provided; these tests
    will be added to the test suite.

    If the settings file has an entry for COVERAGE_MODULES or test_labels is true it will prints the
    coverage report for modules/apps

    Returns number of tests that failed.
    """

    do_coverage = (hasattr(settings, 'COVERAGE_MODULES') or
                   hasattr(settings, 'COVERAGE_APPS') or
                   bool(test_labels))
    if do_coverage:
        coverage.erase()
        coverage.start()
    
    DjangoTestSuiteRunner = None
    try:
        from django.test.simple import DjangoTestSuiteRunner
    except ImportError:
        from django.test import simple
    
    if DjangoTestSuiteRunner:
        testrunner = DjangoTestSuiteRunner(verbosity=verbosity, interactive=interactive, failfast=failfast)
        retval = testrunner.run_tests(test_labels, extra_tests)
    else:
        retval = simple.run_tests(test_labels, verbosity, interactive, extra_tests)

    if do_coverage:
        coverage.stop()

        # Print code metrics header
        print ''
        print '----------------------------------------------------------------------'
        print ' Unit Test Code Coverage Results'
        print '----------------------------------------------------------------------'

        # try to import all modules for the coverage report.
        modules = []
        if test_labels or hasattr(settings, 'COVERAGE_APPS'):
            # apps entered at the command line prompt override those specified in settings
            labels = test_labels or settings.COVERAGE_APPS
            for label in labels:
                label = label.split('.')[0] #remove test class or test method from label
                pkg = _get_app_package(label)
                modules.extend(_package_modules(*pkg))
        elif hasattr(settings, 'COVERAGE_MODULES'):
            modules = [__import__(module, {}, {}, ['']) for module in settings.COVERAGE_MODULES]
        coverage.report(modules, show_missing=1)

    return retval

def _get_app_package(label):
    """Get the package of an imported module"""
    imp, app = [], get_app(label)
    path = os.path.dirname(app.__file__)
    path_list = path.split(os.sep)
    if path_list[-1] == 'models':
        #Models are in a subdirectory, named models.
        #We need to pop this off so that we'll import
        #everything starting at the parent directory.
        path_list.pop()
    path_list.reverse()

    for p in path_list:
        imp.insert(0, p)
        try:
            pkg = __import__('.'.join(imp), {}, {}, [''])
            return pkg, '.'.join(imp)
        except ImportError:
            continue

def _package_modules(pkg, impstr):
    """Get all python modules in pkg including subpackages
    impstr represents the string to import pkg
    """
    modules = []
    path = pkg.__path__[0]
    for f in os.listdir(path):
        if f.startswith('.'):
            continue
        if os.path.isfile(path + os.sep + f):
            name, ext = os.path.splitext(f)
            if ext != '.py' or name == 'admin':
                continue
            #python module
            modules.append(__import__(impstr + '.' + name, {}, {}, ['']))
        elif os.path.isdir(path + os.sep + f):
            #subpackage
            imp = impstr+ '.' + f
            try:
                spkg = __import__(imp, {}, {}, [''])
                modules.extend(_package_modules(spkg, imp))
            except ImportError:
                pass
    return modules

class CoverageTestSuiteRunner(object):
    def __init__(self, verbosity=1, interactive=True, failfast=False, **kwargs):
        self.verbosity = verbosity
        self.interactive = interactive
        self.failfast = failfast

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        print "running tests"
        run_tests(test_labels, verbosity=self.verbosity, interactive=self.interactive,  failfast=self.failfast, extra_tests=None)
