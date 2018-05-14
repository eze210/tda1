#!/bin/bash
cur_dir="${0%/*}"

mkdir img
wget https://raw.githubusercontent.com/eze210/tda1/master/tp2/part2/ej2/img/eq1.png -O img/eq1.png
wget https://raw.githubusercontent.com/eze210/tda1/master/tp2/part2/ej2/img/eq2.png -O img/eq2.png
wget https://raw.githubusercontent.com/eze210/tda1/master/tp2/part2/ej2/img/eq3.png -O img/eq3.png
wget https://raw.githubusercontent.com/eze210/tda1/master/tp2/part2/ej2/img/reduccion-transparente.png -O img/reduccion-transparente.png

pandoc -V geometry:margin=1.25in "$cur_dir/../part1/README.md" \
       "$cur_dir/../part2/ej1/solucion.md" \
       "$cur_dir/../part2/ej2/solution.md" \
       "$cur_dir/../part2/ej3/solution.md" \
       -so doc.tex

pdflatex doc.tex

rm ./doc.aux ./doc.log ./doc.out
rm -R img
