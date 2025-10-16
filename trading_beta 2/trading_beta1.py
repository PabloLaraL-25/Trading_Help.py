import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import ta

# 1. Descargar datos históricos
data = yf.download("AAPL", start="2024-01-01", end="2024-12-31")

# Asegurarse de que close_prices sea una Serie 1D
close_prices = data["Close"].squeeze()

# 2. Calcular indicadores técnicos
data["RSI"] = ta.momentum.RSIIndicator(close_prices).rsi()
macd = ta.trend.MACD(close_prices)
data["MACD"] = macd.macd()
data["Signal"] = macd.macd_signal()
data["EMA"] = ta.trend.EMAIndicator(close_prices, window=20).ema_indicator()

# 3. Mostrar primeras filas
print(data.head())

# 4. Graficar precios + EMA
plt.figure(figsize=(12,6))
plt.plot(close_prices, label="Precio")
plt.plot(data["EMA"], label="EMA 20", linestyle="--")
plt.title("Precio y EMA")
plt.legend()
plt.show()

# 5. Inicializar columnas para señales
data["Senal_Compra"] = None
data["Senal_Venta"] = None

# 6. Lógica de decisión
for i in range(1, len(data)):
    # Señal de compra: RSI < 30 y cruce MACD arriba de Signal
    if (
        data["RSI"].iloc[i] < 30 and
        data["MACD"].iloc[i] > data["Signal"].iloc[i] and
        data["MACD"].iloc[i-1] <= data["Signal"].iloc[i-1]
    ):
        data["Senal_Compra"].iloc[i] = data["Close"].iloc[i]
    # Señal de venta: RSI > 70 y cruce MACD abajo de Signal
    elif (
        data["RSI"].iloc[i] > 70 and
        data["MACD"].iloc[i] < data["Signal"].iloc[i] and
        data["MACD"].iloc[i-1] >= data["Signal"].iloc[i-1]
    ):
        data["Senal_Venta"].iloc[i] = data["Close"].iloc[i]

# 7. Graficar resultados con señales
plt.figure(figsize=(12,6))
plt.plot(data["Close"], label="Precio", color="blue")
plt.plot(data["EMA"], label="EMA 20", linestyle="--", color="orange")
plt.scatter(data.index, data["Senal_Compra"], label="Compra", marker="^", color="green", alpha=1)
plt.scatter(data.index, data["Senal_Venta"], label="Venta", marker="v", color="red", alpha=1)
plt.title("Precio, EMA y Señales de trading")
plt.xlabel("Fecha")
plt.ylabel("Precio")
plt.legend()
plt.show()

