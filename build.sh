#!/bin/bash
prefix="VECTOR-ch"
navigation=$(<navigation.html)
preamble=$(<vector-preamble.html)
footer=$(<vector-footer.html)
chapterTitles=(null FIRST SECOND THIRD FOURTH FIFTH SIXTH SEVENTH EIGHT NINTH TENTH ELEVENTH TWELFTH)

for i in `seq 1 6`; do
    prev=$((i-1));
    next=$((i+1));
    thisNavigation=$navigation
    if ((prev>0))
    then
        thisNavigation=${thisNavigation/"{{prev}}"/$prev};
        thisNavigation=${thisNavigation/"{{prevname}}"/${chapterTitles[prev]}};
        thisNavigation=${thisNavigation/"{{notfirst}}"/};
    else
        thisNavigation=$(sed 's#{{notfirst}}.*</a>##' <<< $thisNavigation);
    fi
    if ((next<13))
    then
        thisNavigation=${thisNavigation/"{{next}}"/$next};
        thisNavigation=${thisNavigation/"{{nextname}}"/${chapterTitles[next]}};
        thisNavigation=${thisNavigation/"{{notlast}}"/};
    else
        thisNavigation=$(sed 's#{{notlast}}.*</a>##' <<< $thisNavigation);
    fi
    echo "$(<vector-preamble.html)$(kramdown "$prefix$i.md")$thisNavigation$(<vector-footer.html)" > "ch$i.html";
    echo "Processed chapter $i";
done