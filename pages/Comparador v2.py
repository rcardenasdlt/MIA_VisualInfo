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
import altair as alt
import pandas as pd

dfScatter5000 = pd.read_csv("./pages/datosComparadorScatter.csv",sep=";")
generosFinal = ['Action', 'Strategy', 'Adventure', 'Indie', 'RPG', 'Simulation', 'Racing', 'Massively Multiplayer', 'Sports']
ordenOwners = [
			'0-20000',
			'20000-50000',
			'50000-100000',
			'100000-200000',
			'200000-500000',
			'500000-1000000',
			'1000000-2000000',
			'2000000-5000000',
			'5000000-10000000',
			'10000000-20000000',
			'20000000-50000000',
			'50000000-100000000',
			'100000000-200000000'
			]

LOGGER = get_logger(__name__)
	

def run():
	st.set_page_config(
		page_title="Recomendador de Videojuegos de Steam",
		page_icon="🎮",
	)
	
	st.write("# Comparador de videojuegos por Horas Jugadas y % Reviews Positivas 🎮")
	
	st.markdown(
		"""
		
		#### Descripción
		Aquí podrás revisar los mejores juegos de Steam donde podras filtrar por popularidad
		y género del videojuego. Puedes resaltar rangos de Owners haciendo click en la leyenda 
		(usando **SHIFT** puedes hacer múltiples selecciones). \n
		Apoyate también seleccionando un rango de fecha y/o precio haciendo **click & drag** en 
		el gráfico correspondiente.\n
		Por la naturaleza de algunos juegos, se aplico logaritmo a las horas jugadas para que 
		la nube no quedara tan dispersa.\n
		\n
		"""
	)
	
	col11, col22, col33 = st.columns(3)
	
	with col11:
		genero = st.selectbox('Choose a genre:',["All"] + generosFinal,key=1)
	with col22:
		categoriaPrecio = st.selectbox('Free to play or Paid:',["Both","Free to play","Paid"],key=2)
	with col33:
		owners = st.selectbox('Number of owners:',["All"] + ordenOwners,key=3)
	
	genero = "Todos" if genero == "All" else genero
	categoriaPrecio = "Todos" if categoriaPrecio == "Both" else categoriaPrecio
	owners = "Todos" if owners == "All" else owners
	
	dfCharts = dfScatter5000[((dfScatter5000.genero == genero) | (genero == "Todos"))
						& ((dfScatter5000.CategoriaPrecio == categoriaPrecio) | (categoriaPrecio == "Todos"))
						& ((dfScatter5000.owners == owners) | (owners == "Todos"))
						]
	
	brush = alt.selection_interval(
		encodings=['x'] # limit selection to x-axis (year) values
	)
	
	selectionOwnerLegend = alt.selection_multi(fields=['owners'], bind='legend')
	
	
	
	# dynamic query histogram
	years = alt.Chart(dfCharts).mark_bar().add_selection(
		brush
	).encode(
		alt.X('release_date:T', title='# Video Games by Release Year'),
		alt.Y('count():Q', title=None),
		
	).properties(
		width=650,
		height=50
	)
	
	# dynamic query histogram
	brushPrecio = alt.selection_interval(
		encodings=['x'] # limit selection to x-axis (year) values
	)
	
	price = alt.Chart(dfCharts).mark_bar(color = "darkolivegreen").add_selection(
		brushPrecio
	).encode(
		alt.X('price:Q', title='# Video Games by Price' ),#,scale=alt.Scale(domain=[0,100]) ),
		alt.Y('count():Q', title=None)#, scale=alt.Scale(domain=[0,300]))
	).properties(
		width=650,
		height=50
	)
	
	#slider = alt.binding_range(min=0, max=1000, step=1, name='Rango Precio:')
	#selectorPrecio = alt.selection_single(name="price", fields=['price'],
	#                                bind=slider, init={'price': 100})
	
	# scatter plot, modify opacity based on selection
	ratings = alt.Chart(dfCharts).mark_circle(size = 80).encode(
		x=alt.X('positiveReviewsPct:Q',title = "Positive Reviews Percentage"),
		y=alt.Y('average_playtime_log:Q', title = "Log of Average Played Time"),
		tooltip=['name:N','release_date:T','developer:N','publisher:N','owners:N','categories:N','genres:N','positive_ratings:Q','negative_ratings:Q','average_playtime:Q', 'price:Q']
		,color = alt.Color('owners:O', scale=alt.Scale(domain=ordenOwners, scheme='purples')
							,legend=alt.Legend(
										orient="none",
										legendX=670, legendY=110,
											)
							)
		,opacity=alt.condition(selectionOwnerLegend, alt.value(0.75), alt.value(0.02))
	).properties(
		width=650,
		height=500,
	).add_selection(
		selectionOwnerLegend
	).transform_filter(
		brush
	).transform_filter(
		brushPrecio
	).interactive()
	
	chartFinalScatter = alt.vconcat(years, ratings, price )#.properties(spacing=5, padding  = 5)
	
	st.altair_chart(chartFinalScatter, use_container_width=True)



if __name__ == "__main__":
	run()