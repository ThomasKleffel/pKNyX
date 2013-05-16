#!/bin/sh

epydoc -o ~/public_html/pKNyX -v -n pKNyX --no-frames --show-imports \
       pknyx/common/*.py \
       pknyx/core/*.py

