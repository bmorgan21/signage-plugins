from distutils.core import setup

setup(
    name='SignagePlugins',
    version='0.1.0',
    author='Brian S Morgan',
    author_email='brian.s.morgan@gmail.com',
    packages=['signage-plugins'],
    url='https://github.com/bmorgan21/signage-plugins',
    description='Integrations for pulling and publishing data to node signage-server.',
    install_requires=[
        'Jinja2>=2.8',
        'requests>=2.8.1',
        'simplejson>=3.8.1'
    ]
)
