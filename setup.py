from distutils.core import setup
import codecs

def long_description():
    with codecs.open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name='Csskrt',
    version='0.1',
    packages=['csskrt'],
    license='MIT',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/4d11/csskrt',
    scripts=['csskrt/main'],
)