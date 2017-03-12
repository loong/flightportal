# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'crawlers',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = crawlers.settings']},
    package_data={
        'crawlers': ['res/*.json']
    },
    zip_safe=False,
    include_package_data = True,
)
