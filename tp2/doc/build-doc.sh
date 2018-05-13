#!/bin/bash
cur_dir="${0%/*}"

pandoc "$cur_dir/../part1/README.md" \
       "$cur_dir/../part2/ej1/solucion.md" \
       "$cur_dir/../part2/ej2/solution.md" \
       "$cur_dir/../part2/ej3/solution.md" \
       -so doc.tex

pdflatex doc.tex

rm ./doc.aux ./doc.tex ./doc.log ./doc.out
