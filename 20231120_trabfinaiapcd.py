# -*- coding: utf-8 -*-
"""20231120_TrabFinaIAPCD.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TJUTlXa9JRa46NSLoU6cGq2iNdLn6tuc

Trabajo Final

información:
https://www.youtube.com/watch?v=ZZsyxIWdCko
"""

# Instalar Streamlit
#!pip install streamlit
# pip install streamlit
#! pip install folium
#! pip install geopandas

#Importar las librerías
#import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import folium
import streamlit as st
#from streamlit_folium import st_folium
import geopandas as gpd
#from streamlit_folium import folium_static

#!wget -q -O - ipv4.icanhazip.com

#! streamlit run app.py & npx localtunnel --port 8501

# cargar los datos del proyecto
df = pd.read_csv('tb_medida_estaciones (1)_0.csv')
df.shape

nansdf = df.isna().sum()

# Mostrar los valores NaN por columna
print(nansdf)

# cargar los datos del código de ubigeo
dfcu = pd.read_csv('TB_UBIGEOS.csv')
dfcu.shape

nansdfcu = dfcu.isna().sum()

# Mostrar los valores NaN por columna
print(nansdfcu)

dfcu_Piura = dfcu.loc[dfcu['departamento'] == 'PIURA']
dfcu_Piura
dfcu_Piura = dfcu_Piura.rename(columns={"ubigeo_inei": "UBIGEO"})

nansPiura = dfcu_Piura.isna().sum()
# Mostrar los valores NaN por columna
print(nansPiura)

# Realizar la fusión de los datasets utilizando el código de ubigeo como clave de relación
df_final = pd.merge(dfcu_Piura, df, left_on='UBIGEO', right_on='UBIGEO')

df_final.shape

nansdf_final = df_final.isna().sum()

print(df_final)

# Filtrar los distritos del departamento de Piura sin repetir
df_piura = df_final['DISTRITO'].unique()

# Crear el mapa con los distritos del departamento de Piura
piura_map = folium.Map(location=[-5.1949, -80.6323], zoom_start=10)  # Coordenadas del centro de Piura

# Marcar los distritos en el mapa con círculos rojos
for distrito in df_piura:
    distrito_data = df_final[df_final['DISTRITO'] == distrito].iloc[0]  # Obtener los datos del primer registro del distrito
    latitud = distrito_data['latitud']
    longitud = distrito_data['longitud']
    folium.CircleMarker(
        location=[latitud, longitud],
        radius=5,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(piura_map)

# Mostrar el mapa
#piura_map

# Crear el dashboard
st.title("Dashboard del Departamento de Piura")
st.markdown("Mapa en dos dimensiones con los distritos del departamento de Piura")
# Mostrar el mapa en el dashboard
st.write(piura_map._repr_html_(), unsafe_allow_html=True)

import matplotlib.pyplot as plt
# Filtra los datos de latitud y longitud para los distritos de Piura
piura_data = df_final[['latitud', 'longitud']]

# Carga el archivo shapefile del contorno del departamento de Piura
peru_mapshp = gpd.read_file("DISTRITOS_inei_geogpsperu_suyopomalia.shp")  # Reemplaza "ruta_del_shapefile.shp" con la ruta de tu archivo shapefile

peru_mapshp.shape

piura_map = peru_mapshp[peru_mapshp['NOMBDEP'] == 'PIURA']

# Crea el plot
fig, ax = plt.subplots(figsize=(5, 10))
# Plotea el mapa del Perú
piura_map.plot(ax=ax, color='lightgray')
# Plotea únicamente el departamento de Piura
piura_map.plot(ax=ax, color='white', edgecolor='black', linewidth=0.5)
# Itera sobre los distritos de Piura y los plotea
for distrito in df_piura:
    distrito_data = df_final[df_final['DISTRITO'] == distrito]
    ax.scatter(distrito_data['longitud'], distrito_data['latitud'], label=distrito)
# Configura los ejes y el título del plot
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
ax.set_title('Departamento de Piura con sus distritos')
# Muestra la leyenda al costado del gráfico
ax.legend(loc='lower left', bbox_to_anchor=(1, 0.62))
# Muestra el plot
plt.show()

# Muestra el plot en el dashboard de Streamlit
st.pyplot(fig)