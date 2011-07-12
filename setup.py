import os

from setuptools import setup
from setuptools import find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name = 'django-test-coverage',
      version = '0.1',
      description = "Get the coverage of your django application.",
      long_description=(
        read('README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
      keywords = 'django test coverage',
      author = 'stj',
      author_email = 'stefan (at) tjarks (dot) de',
#      url = '',
      license = 'MIT',
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Framework :: Django'],
      packages = find_packages('src'),
      package_dir = {'':'src'},
      package_data = {
        '': ['*.txt'],
        },
      namespace_packages=['django-test-coverage'],
      include_package_data = True,
      zip_safe = False,
      install_requires = [
          'setuptools',
	  'Django',
          'coverage',
          ],
      )
