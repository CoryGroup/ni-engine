from distutils.core import setup

setup(
    name='NI Engine',
    version='1.0beta1',
    url='https://github.com/CoryGroup/ni-engine/',
    author='Thomas Alexander and Chris Granade',
    author_email='taalexander@mta.ca',
    package_dir={'': 'src'},
    packages=[
        'ni_engine',
        'ni_engine.config',
        'ni_engine.controllers',
        'ni_engine.hardware',
        'ni_engine.sensors',
        'ni_engine.storage',
        'ni_engine.tools',
    ]
)
