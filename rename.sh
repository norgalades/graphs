#!/bin/bash

#This file takes a directory as argument, parses all the sub-directories inside it to extract the
#AndroidManifest.xml and rename it with the hash of the corresponding file

#$1 is the directory with all the folders for each malware of FamilyX
echo "Parsing directory: "
echo $1
for dir in `ls $1`; do
	path=$1$dir
	cd $path 
	echo "Parsing sub-directory:"
	manifestname=`basename $path .out`
	echo $manifestname
	cp AndroidManifest.xml ./../../manifest/$manifestname
	cd ../..
done
