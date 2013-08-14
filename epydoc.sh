#!/bin/sh

epydoc -o ~/public_html/pKNyX -u http://www.pknyx.org -n pKNyX -v \
       --no-imports --show-frames --graph all --introspect-only \
       pknyx/common pknyx/core pknyx/plugins pknyx/services pknyx/stack pknyx/tools

