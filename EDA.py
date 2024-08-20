import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm, skew, kurtosis

# Configuración de estilo de Seaborn
sns.set(style="whitegrid")

# Conectar a la base de datos
conn = sqlite3.connect('pipeline.db')  # Asegúrate de que este sea el camino correcto a tu base de datos

# Cargar los datos desde la base de datos
query = "SELECT * FROM weather_data"
data = pd.read_sql_query(query, conn)

# Cerrar la conexión
conn.close()

# Filtrar datos para las tres ubicaciones
locations = ["Daniel Flores", "Cartago", "Heredia"]
filtered_data = data[data['city_name'].isin(locations)]

# Calcular estadísticas descriptivas
aqi_stats = filtered_data.groupby('city_name')['aqi'].describe()

# Calcular momentos adicionales
skewness = filtered_data.groupby('city_name')['aqi'].apply(lambda x: skew(x, bias=False))
kurt = filtered_data.groupby('city_name')['aqi'].apply(lambda x: kurtosis(x, bias=False))

moments = pd.DataFrame({'skew': skewness, 'kurtosis': kurt})

# Histograma
plt.figure(figsize=(14, 8))
sns.histplot(data=filtered_data, x='aqi', hue='city_name', kde=True, palette='viridis', bins=30)
plt.title('Distribución del AQI por Ubicación', fontsize=18)
plt.xlabel('AQI', fontsize=14)
plt.ylabel('Frecuencia', fontsize=14)
plt.legend(title='Ubicación')
plt.grid(True)
plt.show()

# Box Plot
plt.figure(figsize=(14, 8))
sns.boxplot(data=filtered_data, x='city_name', y='aqi', palette='viridis')
plt.title('Box Plot del AQI por Ubicación', fontsize=18)
plt.xlabel('Ubicación', fontsize=14)
plt.ylabel('AQI', fontsize=14)
plt.grid(True)
plt.show()

# Time Series Plot
plt.figure(figsize=(16, 8))
for location in locations:
    subset = filtered_data[filtered_data['city_name'] == location]
    plt.plot(subset['datetime'], subset['aqi'], label=location)
plt.title('Serie Temporal del AQI por Ubicación', fontsize=18)
plt.xlabel('Fecha y Hora', fontsize=14)
plt.ylabel('AQI', fontsize=14)
plt.legend(title='Ubicación')
plt.grid(True)
plt.show()

# Ajustar una distribución normal a los datos de AQI de cada ubicación
plt.figure(figsize=(14, 8))
colors = sns.color_palette('viridis', len(locations))
for i, location in enumerate(locations):
    subset = filtered_data[filtered_data['city_name'] == location]
    mean, std = norm.fit(subset['aqi'])
    x = np.linspace(subset['aqi'].min(), subset['aqi'].max(), 100)
    p = norm.pdf(x, mean, std)
    plt.plot(x, p, label=f'{location} (mean={mean:.2f}, std={std:.2f})', color=colors[i])
plt.title('Ajuste de Distribución Normal del AQI por Ubicación', fontsize=18)
plt.xlabel('AQI', fontsize=14)
plt.ylabel('Densidad de probabilidad', fontsize=14)
plt.legend(title='Ubicación')
plt.grid(True)
plt.show()

# Crear DataFrame para la tabla de momentos
moments_table = pd.DataFrame({
    'Media': filtered_data.groupby('city_name')['aqi'].mean(),
    'Varianza': filtered_data.groupby('city_name')['aqi'].var(),
    'Desviación Estándar': filtered_data.groupby('city_name')['aqi'].std(),
    'Inclinación (Skewness)': skewness,
    'Kurtosis': kurt
})
moments_table.to_csv('moments_table.csv')

print(moments_table)

