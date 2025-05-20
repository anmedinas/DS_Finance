set title "Matriz de Correlación"
set size square
unset key
set xrange [0.5:*]
set yrange [0.5:*]
set xtics out
set ytics out
set cblabel "Correlación"
set palette defined (0 "blue", 0.5 "white", 1 "red")
set cbrange [-1:1]
set terminal qt size 800,800
plot "correlation_matrix.txt" using 1:2:3 with image pixels
