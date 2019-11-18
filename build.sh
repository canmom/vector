#!/bin/bash
prefix="VECTOR-ch"

for i in `seq 1 6`; do
  kramdown "$prefix$i.md" | cat vector-preamble.html - vector-footer.html > "ch$i.html"; 
done