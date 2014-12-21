# coding: utf-8

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

setup(
    name  = 'dalmatian',
    version = '0.1.0',
    description = 'Visualizing a confusion matrix with gradations',
    license = 'MIT',
    author = 'Shoya Ishimaru',
    author_email = 'shoya.ishimaru@gmail.com',
    url = 'https://github.com/shoya140/dalmatian',
    keywords = 'confusion matrix',
    packages = find_packages(),
    install_requires = ['numpy', 'reportlab'],
    classifiers = [
      'Programming Language :: Python :: 2.7',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: MIT License'
    ]
)