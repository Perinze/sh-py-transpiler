#!/bin/dash

if test -r /dev/null
then
    echo r
fi

if test -w /dev/null
then
    echo w
fi

if test -x /dev/null
then
    echo x
fi