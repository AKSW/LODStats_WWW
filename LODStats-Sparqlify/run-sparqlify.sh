#!/bin/bash
#default port: 7531
sparqlify -h localhost -u postgres -p postgres -d lodstats -m lodstats.sml
