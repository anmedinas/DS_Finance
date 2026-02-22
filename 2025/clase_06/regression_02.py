import yfinance as yf
import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import seaborn as sns 

sns.set_style("dark")

# Descargar los datos
bond_price = yf.download('TLT', start='2015-01-01', end='2024-01-01')['Close']
t10y = web.DataReader('GS10', 'fred', '2015-01-01', '2024-01-01')

# Resampleo mensual
bond_monthly = bond_price.resample('M').last()
t10y_monthly = t10y.resample('M').last()

# Merge
df = pd.concat([bond_monthly, t10y_monthly], axis=1)
df.columns = ['Precio_TLT', 'Tasa10Y']
df = df.dropna()

# Preparar datos
X = df['Tasa10Y'].values.reshape(-1, 1)
y = df['Precio_TLT'].values

# Ajustar modelo de regresión
modelo = LinearRegression()
modelo.fit(X, y)
y_pred = modelo.predict(X)

# Gráfico con estilo personalizado
plt.figure(figsize=(8, 6))
plt.title("Relación entre Tasa 10Y y Precio TLT", fontsize=14)
plt.xlabel("Tasa 10Y (%)", fontsize=12)
plt.ylabel("Precio del ETF TLT (USD)", fontsize=12)

# Scatter de datos
plt.scatter(X, y,  zorder=3)

# Línea de regresión
x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_range = modelo.predict(x_range)
plt.plot(x_range, y_range, color='blue', linewidth=2, label='Regresión lineal')

# Líneas de error (residuos)
for i in range(len(X)):
    plt.plot([X[i], X[i]], [y[i], y_pred[i]], color='red', linewidth=1)

# Invertir eje x para visualización más intuitiva (tasa ↑ → precio ↓)
#plt.gca().invert_xaxis()

plt.legend()
plt.tight_layout()
plt.savefig("scatterplot2.png", dpi = 300, bbox_inches = 'tight', transparent = False)
plt.show()