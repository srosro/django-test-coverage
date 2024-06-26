# -*- coding: utf-8 -*-
#working on django 1.6 and python 3.3.2 as of 11-20-13 
import sys
import os
import webbrowser
import traceback
from os.path import exists, isdir, abspath, join

from django.apps import apps
from django.conf import settings

from coverage import coverage

__valid_browser_open_types = {
    'existing': 0,
    'window': 1,
    'tab': 2
}

if sys.version <= '3.3':
    print("this version only supports python 3.x.x and django 2.1 and above")
    print("results not guaranteed on other versions")
    

__valid_browser_open_types_str = ', '.join(__valid_browser_open_types.keys())

### coverage reporters ###
def reporter_console(cov, modules):
    """
    Generates a report to stdout
    """
    # Print code metrics header
    print ('')
    print ('----------------------------------------------------------------------')
    print (' Unit Test Code Coverage Results')
    print ('----------------------------------------------------------------------')
    cov.report(modules, show_missing=1)

def reporter_xml(cov, modules):
    """
    Generates an xml report

    The following values from django's settings are used:

    COVERAGE_XML_FILE: Specifies the output path or outputs to coverage.xml if
                       not specified.
    """
    #if None, just outputs to stdout
    outfile = getattr(settings, 'COVERAGE_XML_FILE', None)
    print ('Writing XML report')
    cov.xml_report(modules, outfile)
    print ('Done')

def reporter_html(cov, modules):
    """
    Generates a html report

    The following values from django's settings are used:

    COVERAGE_HTML_DIRECTORY: Directory to output html to; defaults to covhtml
                             in the current directory. If the directory doesn't
                             exist it'll be created.
    COVERAGE_HTML_EXTRA_CSS: An extra css file that coverage'll copy into the
                             output directory if given; defaults to None.
    COVERAGE_HTML_OPEN_IN_BROWSER: Whether or not to open the index file after
                                   generation. Uses the webbrowser module to do
                                   so. Default is False.
    COVERAGE_HTML_BROWSER_OPEN_TYPE: If COVERAGE_HTML_OPEN_IN_BROWSER is True,
                                     then this dictates how the open is done.
                                     Possible values are 'existing' (use
                                     existing browser window), 'new' (try and
                                     open a new browser), or 'tab' (python >=
                                     2.5 only; attempts to open in a new tab).
                                     See
                                     http://docs.python.org/library/webbrowser.html#webbrowser.open
                                     for details.
    """
    open_in_browser = getattr(settings, 'COVERAGE_HTML_OPEN_IN_BROWSER', False)
    covdir = abspath(getattr(settings, 'COVERAGE_HTML_DIRECTORY', 'covhtml'))
    extra_css = getattr(settings, 'COVERAGE_HTML_EXTRA_CSS', None)
    open_type = getattr(settings, 'COVERAGE_HTML_BROWSER_OPEN_TYPE', 'existing')
    open_type = __valid_browser_open_types.get(open_type)
    if open_type is None:
        print ('%s is not a valid value for COVERAGE_HTML_BROWSER_OPEN_TYPE; valid values: %s' % (open_type,
                                                                                                         __valid_browser_open_types_str))
                #open_in_browser = False

    if not exists(covdir):
        print ("COVERAGE_HTML_DIRECTORY (%s) doesn't exist; creating" % covdir)
        os.mkdir(covdir)
    else:
        if not isdir(covdir):
            print ('Not writing HTML report; COVERAGE_HTML_DIRECTORY (%s) points to a non-directory' % covdir)
            return
        elif not os.access(covdir, os.W_OK):
            print ("Not writing HMTL report; COVERAGE_HTML_DIRECTORY (%s) isn't writable" % covdir)
            return

    print ('Writing html report')
    cov.html_report(modules, extra_css=extra_css, directory=covdir)
    print ('Done')
    if open_in_browser:
        #XXX will this work in windows since it uses \ as a separator?
        if not webbrowser.open('file://%s' % join(covdir, 'index.html'),
                               new=open_type):
            print ('Unable to open coverage index in webbrowser')

_cov_reporters = {
    'console': reporter_console,
    'html': reporter_html,
    'xml': reporter_xml,
}

_valid_covtypes_str = ', '.join(_cov_reporters.keys())

class CoverageTestSuiteRunner(object):
    def __init__(self, verbosity=1, interactive=True, failfast=False, **kwargs):
        self.verbosity = verbosity
        self.interactive = interactive
        self.failfast = failfast


    def run_tests(self, test_labels, extra_tests=None, **kwargs):
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
    
        You can control coverage's output via the COVERAGE_REPORT_TYPE variable;
        possible values are 'console' (default, output to stdout), 'html' (outputs
        html to the directory specified by COVERAGE_HTML_DIRECTORY) or 'xml'
        (outputs an xml file to COVERAGE_XML_FILE).
    
        Returns number of tests that failed.
        """
    
        cov = None
        do_coverage = (hasattr(settings, 'COVERAGE_MODULES') or
                       hasattr(settings, 'COVERAGE_APPS') or
                       bool(test_labels))
        if do_coverage:
            cov = coverage()
            cov.erase()
            cov.start()
    
        DiscoverRunner = None
        try:
            from django.test.runner import DiscoverRunner
        except ImportError:
            raise
    
        try:
            if DiscoverRunner:
                testrunner = DiscoverRunner(verbosity=self.verbosity, interactive=self.interactive, failfast=self.failfast)
                retval = testrunner.run_tests(test_labels, extra_tests)
        except Exception:
            #if we don't print the exc here, nothing'll be outputted to the terminal
            print ('An error occured while attempting to run the tests:')
            traceback.print_exc()
            raise
    
        if do_coverage:
            cov.stop()
    
            covtype = getattr(settings, 'COVERAGE_REPORT_TYPE', 'console')
            cov_reporter = _cov_reporters.get(covtype)
            if not cov_reporter:
                raise RuntimeError('Invalid COVERAGE_REPORT_TYPE given: %s; valid values: %s' % (covtype,
                                                                                                 _valid_covtypes_str))
    
            # try to import all modules for the coverage report.
            modules = []
            if test_labels or hasattr(settings, 'COVERAGE_APPS'):
                # apps entered at the command line prompt override those specified in settings
                labels = test_labels or settings.COVERAGE_APPS
                for label in labels:
                    label_split = label.split('.')
                    if len(label_split) > 1:
                        label = label_split[:-1]  # remove test class or test method from label
                        label = '.'.join(label)
                    pkg = _get_app_package(label)
                    modules.extend(_package_modules(*pkg))
            elif hasattr(settings, 'COVERAGE_MODULES'):
                modules = [__import__(module, {}, {}, ['']) for module in settings.COVERAGE_MODULES]
    
    
            if hasattr(settings, 'COVERAGE_EXCLUDE_MODULES'):
                for exclude_module_name in settings.COVERAGE_EXCLUDE_MODULES:
                    # Test designed to avoid accidentally removing a module whose
                    # name is prefixed by an excluded module name, but still remove
                    # submodules
                    modules = [module for module in modules
                        if not module.__name__ == exclude_module_name and
                        not module.__name__.startswith(exclude_module_name + '.')]
    
            cov_reporter(cov, modules)
    
        return retval

def _get_app_package(label):
    """Get the package of an imported module"""
    imp, app = [], apps.get_app_config(label)
    path_list = app.path.split(os.sep)

    if path_list[-1] == 'models':
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

    
    path = list(pkg.__path__)[0]
    files = os.listdir(path)
    for f in files:
        
        if f.startswith('.'):
            continue
        test_me = path+os.sep+f
        if os.path.isdir(test_me) and f != '__pycache__':
            #subpackage

            imp = impstr+ '.' + f
            try:
                spkg = __import__(imp, {}, {}, [''])
                modules.extend(_package_modules(spkg, imp))
            except ImportError:
                pass
        elif os.path.isfile(test_me):
            name, ext = os.path.splitext(f)
            if ext != '.py' or name == 'admin':
                continue
            #python module
            modules.append(__import__(impstr + '.' + name, {}, {}, ['']))
        
    return modules


__all__ = ['CoverageTestSuiteRunner']
