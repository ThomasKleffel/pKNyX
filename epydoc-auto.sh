#!/bin/sh

echo -n "Directory to generate the documentation [`pwd`doc/] "
read DIR
if [ -z $DIR ]; then
    DIR=`pwd`/doc/
fi

echo -n "Generate documentation in $DIR [Y/n] "
read rep
if [ -z $rep ]; then
    rep=Y
fi

case $rep in
    Y|YES|y|yes)
        epydoc  -o $DIR -n pKNyX --ignore-param-mismatch --no-frames \
        --show-imports --private-css blue --inheritance Grouped  ../
        ;;
esac

