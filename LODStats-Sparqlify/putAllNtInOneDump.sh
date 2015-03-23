#!/bin/bash

NTFILES=./void/*.nt

for f in $NTFILES
do
  test -f "$f" && echo "$f" >> /tmp/merged && cat "$f" >> /tmp/merged.nt;
done
