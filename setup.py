import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()


setup(
    name='django-keeper',
    version='0.1.7',
    install_requires=[
        'Django>=1.10,<2.1',
    ],
    author='Hiroki KIYOHARA',
    author_email='hirokiky@gmail.com',
    url='https://github.com/hirokiky/django-keeper/',
    license='MIT',
    description="Authorization library for Django, with ACL, not depends on models.",
    long_description=README,
    test_suite="tests",
    packages=['keeper', 'keeper.templatetags'],
)
