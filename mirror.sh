#!/bin/sh

wget \
 --recursive \
 --no-clobber \
 --page-requisites \
 --html-extension \
 --convert-links \
 --restrict-file-names=windows \
 --domains www.ztflh.com \
 --no-parent \
     www.ztflh.com
