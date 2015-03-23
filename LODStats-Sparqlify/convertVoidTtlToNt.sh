#!/bin/bash

TTLFILES=./void/*.ttl

for f in $TTLFILES
do
  echo "Processing $f ..."
  rapper -i turtle -o ntriples $f > $f.nt
done
