from setuptools import setup, find_packages
import codecs

def long_description():
    with codecs.open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name='csskrt',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/4d11/csskrt',
    entry_points='''
        [console_scripts]
        csskrt=main:freshify
    ''',
)