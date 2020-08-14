from setuptools import setup

setup(
    name='htrack',
    version='0.1',
    py_modules=['htrack'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        htrack=htrack:cli
    ''',
)

