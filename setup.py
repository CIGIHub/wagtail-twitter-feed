import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='wagtail-twitter-feed',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "django",
        "wagtail",
        "tweet_cache",
    ],
    dependency_links=[
        "git+https://github.com/CIGIHub/tweet_cache.git#egg=tweet_cache"
    ],
    include_package_data=True,
    license='MIT License',
    description='Django app for wagtail site that adds twitter feed data.',
    long_description=README,
    url='https://github.com/CIGIHub/wagtail-twitter-feed',
    author='Caroline Simpson',
    author_email='csimpson@cigionline.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
