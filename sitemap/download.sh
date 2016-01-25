#!/bin/bash

# from https://www.XYZ.com/robots.txt
for i in {1..1000}
do
    wget http://www.XYZ.com/sitemap.$i.xml.gz
done
