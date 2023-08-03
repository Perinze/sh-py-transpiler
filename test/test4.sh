#!/bin/dash

string=BAR
echo FOO${string}BAZ

string1=FOO${string}BAZ
echo $string1
