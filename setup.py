from setuptools import setup, find_packages
import codecs
import os

def long_description():
    here = os.path.dirname(os.path.abspath(__file__))
    with codecs.open(os.path.join(here, 'README.md'), encoding='utf8') as f:
        return f.read()


setup(
    name='csskrt-csskrt',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    #  long_description=long_description(), #todo getting file error need to fix
    author='4d11',
    url='https://github.com/4d11/csskrt-csskrt',
    keywords='css bootstrap bulma csskrt skrrt',
    entry_points='''
        [console_scripts]
        csskrt=csskrt.main:freshify
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities'
    ],
    install_requires=[
        'click',
        'beautifulsoup4',
    ]
)
