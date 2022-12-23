import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()


setup(
    name='django-keeper',
    version='0.4.0',
    install_requires=[
        'Django>=2.2,<4.2',
    ],
    author='Hiroki KIYOHARA',
    author_email='hirokiky@gmail.com',
    url='https://github.com/hirokiky/django-keeper/',
    license='MIT',
    description="Authorization library for Django, with ACL, not depends on models.",
    long_description=README,
    long_description_content_type='text/markdown',
    test_suite="tests",
    packages=['keeper', 'keeper.templatetags'],
)
