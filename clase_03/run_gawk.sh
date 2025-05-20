#!/bin/bash

INPUT="stocks.csv"
MATRIX="correlation_matrix.txt"
GNUPLOT_SCRIPT="plot_corr.gnuplot"

# Paso 1: Calcular matriz de correlación con gawk (separador ;)
gawk -F";" '
BEGIN {
    OFS = "\t"
}
NR==1 {
    for (i=1; i<=NF; i++) {
        colname[i] = $i
    }
    num_cols = NF
    next
}
{
    for (i=1; i<=num_cols; i++) {
        if ($i != "") {
            data[NR-1,i] = $i + 0
            sum[i] += data[NR-1,i]
            sumsq[i] += data[NR-1,i] * data[NR-1,i]
        }
    }
    N++
}
END {
    for (i=1; i<=num_cols; i++) {
        mean[i] = sum[i] / N
        for (j=1; j<=num_cols; j++) {
            cov = 0
            for (k=1; k<=N; k++) {
                cov += (data[k,i] - mean[i]) * (data[k,j] - mean[j])
            }
            cov /= (N - 1)
            std_i = sqrt(sumsq[i]/N - mean[i]^2)
            std_j = sqrt(sumsq[j]/N - mean[j]^2)
            corr[i,j] = (std_i && std_j) ? cov / (std_i * std_j) : 0
        }
    }

    # Output formato: fila columna correlación
    for (i=1; i<=num_cols; i++) {
        for (j=1; j<=num_cols; j++) {
            print i, j, corr[i,j]
        }
    }
}
' "$INPUT" > "$MATRIX"

# Paso 2: Crear script de gnuplot que solo muestre la matriz en pantalla
cat <<EOF > $GNUPLOT_SCRIPT
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
plot "$MATRIX" using 1:2:3 with image pixels
EOF

echo "✅ Matriz generada: $MATRIX"
echo "✅ Script de gnuplot generado: $GNUPLOT_SCRIPT"
echo "👉 Ejecuta: gnuplot -persist $GNUPLOT_SCRIPT"