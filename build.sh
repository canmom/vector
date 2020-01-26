#!/bin/bash
prefix="VECTOR-ch"
navigation=$(<navigation.html)
chapterTitles=(null FIRST SECOND THIRD FOURTH FIFTH SIXTH SEVENTH EIGHT NINTH TENTH ELEVENTH TWELFTH)
nChapters=$1;
nLinked=$2;

for i in `seq 1 $nChapters`; do
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
    if ((i<nLinked))
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

pandoc epub-meta.txt VECTOR-ch*.md -o VECTORch1-$nChapters.epub --epub-chapter-level=2 --top-level-division=chapter;
echo "Generated epub"

zip VECTORch1-$nChapters.zip ch*.html index.html style.css illustration-titled.png logo.svg
echo "Zipped page for itch.io"