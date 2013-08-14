from distutils.core import setup

setup(
    name='NI Engine',
    version='1.0beta1',
    url='https://github.com/CoryGroup/ni-engine/',
    author='Thomas Alexander and Chris Granade',
    author_email='taalexander@mta.ca',
    package_dir={'': 'src'},
    packages=[
        'config',
        'controllers',
        'hardware',
        'ni_engine',
        'sensors',
        'storage',
        'tools',
    ]
)
