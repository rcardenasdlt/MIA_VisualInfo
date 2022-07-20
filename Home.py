# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)
	

def run():
	st.set_page_config(
		page_title="Recomendador de Videojuegos de Steam",
		page_icon="🎮",
	)

	st.write("# Bienvenidos a mi Streamlit! 🎮")

	st.markdown(
		"""
		Este streamlit esta orientado al proyecto final del ramo
		de **Visualización de Información y Analítica Visual** del 
		Magister de Inteligencia Artificial (PUC 2021).\n
		**Desarrollado por Rodrigo Cárdenas (rdcardenas@uc.cl,rcardenasdlt@gmail.com).**
		## Recomendador de Videojuegos
		### **Caracterización del dominio**
		En este proyecto se uso una base de videojuegos de Steam (2019),
		extraída de [Kaggle](https://www.kaggle.com/datasets/nikdavis/steam-store-games).\n
		**Problema:** Brindar apoyo a la selección de compra o
		adquisición de un videojuego.\n
		**Usario:** Público general.
		### **Abstracción de datos y tareas**
		
		#### Datos
		**Items:** Cada registro es un videojuego que es vendido en la 
		plataforma de Steam.\n
		**Atributos:**
		- **appid:** ID de videojuego en Steam
		- **name:** Nombre del videojuego
		- **release_date:** Fecha de lanzamiento
		- **english:** Si el juego esta disponible en ingles
		- **developer:** Desarrollador del videojuego
		- **publisher:** Publicador del videojuego
		- **platforms:** OS donde es ejecutable el videojuego
		- **required_age:** Edad sugerida
		- **categories:** Categorias asociadas al videojuego (FPS,MMO,etc.)
		- **genres:** Genero del videojuego (Acción,RPG,etc.)
		- **steamspy_tags:** Tags de Steam
		- **achievements:** Indicador si el juego tiene "Logros"
		- **positive_ratings:** Número de reviews positivos
		- **negative_ratings:** Número de reviews negativos
		- **average_playtime:** Promedio de horas de tiempo jugado
		- **median_playtime:** Mediana de horas de tiempo jugado
		- **owners:** Cantidad de usuarios Steam que poseen el videojuego (ramificado)
		- **price:** Precio del videojuego en el momento de medición
		
		#### Tarea
		Presentar y comparar las opciones del portafolio de videojuegos 
		que proporciona Steam de forma sencilla para facilitar la decisión
		al usuario final.
		
		### **Codificación visual**
		Debido al gran abanico de opciones, se decidió generar un 
		scatterplot con los ejes mas relevantes de indicador de un
		videojuego (a criterio del editor) y filtros para hacer una
		busqueda mas personalizada a criterio del usuario.
		
		En la segunda entrega se realizará un gráfico de barras (con filtros)
		mostrando los top N según criterio del editor (Editor's Choice).
		
		Fecha de creación: 19/07/2022
	"""
	)


if __name__ == "__main__":
	run()