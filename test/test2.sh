#!/bin/dash

if test -e /dev/null
then
    echo e
fi

if test -f /dev/null
then
    echo f
fi

if test -d /dev/null
then
    echo d
fi

if test -d /dev
then
    echo d
fi