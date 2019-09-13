#!/bin/bash
prefix="VECTOR-ch"

for i in `seq 1 5`; do
  kramdown "$prefix$i.md" | cat vector-preamble.html - vector-footer.html > "$prefix$i.html"; 
done