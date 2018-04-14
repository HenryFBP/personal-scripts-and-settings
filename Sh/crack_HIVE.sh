#!/bin/sh -x

windowsSAMdir="/Windows/System32/config/"
filename="~/Desktop/samdump.txt"
tempname="~/Desktop/samdump.tmp"

 # turn tilde into dir
eval filename=$filename
eval tempname=$tempname

# make sure files exist
touch $filename
touch $tempname

samdump2 SYSTEM SAM -o $tempname # output to temp file

cat $tempname >> $filename # append to main file 

sort $filename > $tempname #sort file

cat $tempname | uniq > $filename #remove dupe lines

gnome-terminal -- john $filename -format=nt
