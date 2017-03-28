#!/usr/bin/env python
# -*- coding: utf-8 -*

"""Generating/updating project related files"""

import hashlib
import re
import os
import binascii
import datetime
import time
import hashlib

files = [
    'tournament.py',
    'tournament.sql',
    'tournament_test.py',
    'README.md-template'
]

md5 = hashlib.md5()

file_index = []
for file_name in files:
    md5.update(open(file_name).read())
    file_index.append("`" + file_name + " (md5: " + binascii.hexlify(md5.digest()) + ")`")


genrated = datetime.datetime.now().isoformat()

readme_template = open("README.md-template").read()
readme = readme_template.format(
    files="* " + ("\n* ").join(file_index),
    genrated=genrated
)

readme_file = open("README.md","w+")
readme_file.write(readme)
readme_file.close()
