#!/bin/bash
file_name=$1
subject_name=`echo $file_name | cut -d"_" -f2` 
line='{print "'${subject_name},'" $0}'
str="'$line' ${file_name}"
cmd="awk -F\",\" $str >> lrta_subs.csv"
echo $cmd

