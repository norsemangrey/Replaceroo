from setuptools import setup

setup(
    name="replaceroo",
    version='1.0',
    packages=['replaceroo'],
    description="A program for replacing multiple strings in a text file using a reference list.",
    author="Jan Magnus Røkke",
    author_email="jan.magnus.roekke@gmail.com",
    license="Private",
    keywords="search, replace, list",
    entry_points={
        'console_scripts': [
            'replaceroo = replaceroo.replaceroo'
        ]
    }
    )
