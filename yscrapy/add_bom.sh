#!/usr/bin/env bash
#Add BOM to the new file
printf '\xEF\xBB\xBF' > with_bom.txt
cat company.csv >> with_bom.txt
rm -f with_bom.txt
