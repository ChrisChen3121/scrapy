#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import codecs

with open('bom_company.csv', mode='w') as bom_file:
    bom_file.write(codecs.BOM_UTF8)
    with open('company.csv', mode='r') as comp_file:
        bom_file.write(comp_file.read())
