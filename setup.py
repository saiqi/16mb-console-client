from setuptools import setup, find_packages

setup(
    name='16mb-console-client',
    version='0.0.1',
    packages=find_packages(exclude=['tests', 'tests.*']),
    url='http://github.com/saiqi/16mb-console-client',
    license='',
    author='Julien Bernard',
    author_email='julien.bernard.iphone@gmail.com',
    description='16 Megabytes console client',
    install_requires=[
        'PyJWT==1.5.3',
        'PyYAML==3.12',
        'requests==2.20.0',
        'terminaltables==3.1.0'
    ],
    extra_requires={
        'dev': [
            'pytest==3.2.3',
            'pytest-mock==1.6.3'
        ]
    },
    entry_points={
        'console_scripts': [
            '16mbctl=console_client.main:main'
        ]
    }
)
