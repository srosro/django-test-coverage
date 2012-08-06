from setuptools import setup, find_packages

version = '0.1'

description = '''
A fork of django-test-coverage 0.1 (http://pypi.python.org/pypi/django-test-coverage/) with bugfixes.
'''

setup(
    name='django-test-coverage',
    version=version,
    description='django-test-coverage',
    long_description=description,
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
    keywords='django,test,coverage,fork',
    url='http://github.com/srosro/django-test-coverage'
    license='MIT',
    packages=['django_test_coverage'],
    install_requires=['coverage'],
    include_package_data=True,
    zip_safe=False,
)

