#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(name='poker_stats',
      version='0.1.0.dev2',
      author='Polish Poker Community in Manila',
      author_email='dev@null.com',
      url='https://github.com/yarpenzigrin/pokerstats',
      description='Statistics generator for poker hands played online',
      long_description='Statistics generator for poker hands played online\nUnder construction',
      license='MIT',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7'],
      packages=find_packages(exclude=['test', 'test.ut']),
      entry_points={'console_scripts':['poker_stats = poker_stats:main']},
      python_requires='>=2.7, <3',
      install_requires=['enum34==1.1.6', 'pyparsing==2.1.10', 'Flask==0.12.2', 'gunicorn==19.7.1']
)
