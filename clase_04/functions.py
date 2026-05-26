from matplotlib import pyplot as plt
import seaborn as sns
import yfinance as yf
import numpy as np
from scipy.stats import norm, t, probplot


def plot_stock_returns_with_distribution(ticker, start_date, end_date):
    # Descargar datos de la serie financiera
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    # Calcular los retornos logarítmicos
    data['Returns'] = np.log(data['Close'] / data['Close'].shift(1)).dropna()

    # Eliminar el primer valor nulo
    returns = data['Returns'].dropna()

    # Crear subplots: uno para la serie de precios, otro para el histograma de retornos, y el Q-Q plot
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    # Subplot 1: Serie histórica de precios
    ax1.plot(data['Close'], label='Serie histórica de precios')
    ax1.set_title(f'Serie histórica de precios: {ticker}')
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel('Precio ajustado')
    ax1.legend()

    # Subplot 2: Histograma de retornos
    ax2.hist(returns, bins=50, density=True, alpha=0.6, color='blue', label='Retornos')

    # Ajuste a una distribución normal
    mu, std = norm.fit(returns)
    xmin, xmax = ax2.get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    ax2.plot(x, p, 'k', linewidth=2, label='Normal')

    # Ajuste a una distribución t-Student
    df, loc, scale = t.fit(returns)
    p_t = t.pdf(x, df, loc, scale)
    ax2.plot(x, p_t, 'r', linewidth=2, label=f't-Student (df={df:.2f})')

    # Título y leyenda del histograma
    ax2.set_title('Histograma de retornos y ajuste a distribuciones')
    ax2.set_xlabel('Retornos')
    ax2.set_ylabel('Densidad')
    ax2.legend()

    # Subplot 3: Q-Q plot de los retornos
    probplot(returns, dist="norm", plot=ax3)
    ax3.set_title('Q-Q plot de los retornos')
    ax3.set_xlabel('Quantiles teóricos')
    ax3.set_ylabel('Quantiles de los retornos')

    # Ajustar el layout y mostrar gráficos
    plt.tight_layout()
    plt.show()