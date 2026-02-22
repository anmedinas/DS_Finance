import yfinance as yf
import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_style("dark")

bond_price = yf.download('TLT', start = '2015-01-01', end = '2024-01-01', progress = False)['Close']
t10y = web.DataReader('GS10', 'fred', '2015-01-01', '2024-01-01')

bond_monthly = bond_price.resample('M').last()
t10y_monthly = t10y.resample('M').last()
df = pd.concat([bond_monthly, t10y_monthly], axis=1)
df.columns = ['Precio_Bono_TLT', 'Tasa10Y']
df = df.dropna()

plt.figure(figsize = (8, 6))
plt.scatter(df['Tasa10Y'], df['Precio_Bono_TLT'], alpha = 0.7)
plt.title('Precio del bono (TLT) vs Tasa de interés 10Y')
plt.xlabel('Tasa de Interés 10Y (%)')
plt.ylabel('Precio del ETF TLT ($)')
plt.savefig("scatterplot.png", dpi = 300, bbox_inches = 'tight', transparent = False)
plt.show()