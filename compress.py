# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 02:21:47 2016

@author: Alberto
"""

# Example of how to GZIP compress an existing file:

import gzip
import shutil
file_name = 'ULCL_An_Ultra-Lightweight_Cryptographic.pdf'
with open(file_name, 'rb') as f_in, gzip.open(file_name + '.gz', 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)