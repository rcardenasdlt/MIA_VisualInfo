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

dfEditorsChoice = pd.read_csv("./pages/datosEditorsChoice.csv",sep=";")
generosFinal = ['All','Action', 'Strategy', 'Adventure', 'Indie', 'RPG', 'Simulation', 'Racing', 'Massively Multiplayer', 'Sports']
ordenOwners = [ "All",
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
	
	st.write("# Editor's Choice - Videojuegos altamente recomendados 🎮")
	
	st.markdown(
		"""
		#### Descripción
		Estos son los videojuegos que deberían considerar si es que no los has jugado aún.\n
		El score es el número de reviews positivas que tiene el videojuego castigado
		levemente por el número de reviews negativas (siendo que muchos problemas son arreglados por actualizaciones
		de éste mismo y hay juegos muy buenos con opiniones dispersas).\n
		Disfruten!\n
		"""
	)
	col1, col2, col3,col4 = st.columns(4)
	
	with col1:
		genero = st.selectbox('Choose a genre:',generosFinal)
	with col2:
		categoriaPrecio = st.selectbox('Free to play or Paid:',["Both","Free to play","Paid"])
	with col3:
		owners = st.selectbox('Number of owners:',ordenOwners)
	with col4:
		nResultados = st.slider(
		"# Results", min_value=5 , max_value=100, step=1, value=10
		)
	
	genero = "Todos" if genero == "All" else genero
	categoriaPrecio = "Todos" if categoriaPrecio == "Both" else categoriaPrecio
	owners = "Todos" if owners == "All" else owners
	
	barSize = 30
	chartFinal = alt.Chart(
		dfEditorsChoice[(dfEditorsChoice.genero == genero)
						& ((dfEditorsChoice.CategoriaPrecio == categoriaPrecio) | (categoriaPrecio == "Todos"))
						& ((dfEditorsChoice.owners == owners) | (owners == "Todos"))
						]
		,height = alt.Step(barSize*1.2)
	).mark_bar(size = barSize).encode(
		x=alt.X('Score:Q',title = None),
		y=alt.Y('name:N' 
				, sort='-x'
				,axis=alt.Axis(domainOpacity=0, ticks=False
							  ,title=""
							  #,labelFont = "sans-serif"
							  ,labelFontSize = 12
							  #,labelColor= "#7d7d7d"
							  ,labelFontStyle='bold'
							  )
				,title=None)
		,tooltip=['name:N','release_date:T','developer:N','publisher:N','owners:N','categories:N','genres:N','positive_ratings:Q','negative_ratings:Q','average_playtime:Q', 'price:Q']
		,color=alt.Color('Score:Q')
	).transform_window(
		rank='rank(Score)',
		sort=[alt.SortField('Score', order='descending')]
	).transform_filter(
		(alt.datum.rank <= nResultados)
	)#.configure_scale(bandPaddingInner=0.9)

	
	
	
	st.altair_chart(chartFinal, use_container_width=True)



if __name__ == "__main__":
	run()