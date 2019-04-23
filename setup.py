import sys
from setuptools import setup, find_packages

requires = [
    'requests==2.20.1',
    'beautifulsoup4==4.7.1',
    'bs4==0.0.1',
    'jsonpickle==1.1'
]

setup(
    name='google-play-reviews-scraper',
    version='0.1.0',
    description=("Google-play-reviews-scraper is a command-line application written in Python"
                 " that scrapes and downloads an apps user reviews."),
    url='https://github.com/mohamedali92/google-play-reviews-scraper',
    author='Mohamed Ali',
    author_email='mohamed.ali@alumni.ubc.ca',
    license='Public domain',
    packages=find_packages(exclude=['tests']),
    install_requires=requires,
    zip_safe=False,
)