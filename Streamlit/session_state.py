import streamlit as st
import pandas as pd
from functions import *
import altair as alt
from datetime import datetime, timedelta

# Lista de opções de ativos
assets_options = ['PETR4.SA', 'ITUB4.SA', 'BBDC4.SA']

# Filtro de seleção do ativo
asset_filter = st.radio("Pick a Asset!", options=assets_options, key='asset')
st.write(f"You selected: {asset_filter}")

# Configuração das datas
max_date = datetime.now()
min_date = max_date - timedelta(days=365 * 5)

min_date_input = st.date_input("Min Date", min_date, min_value=min_date, max_value=max_date)
max_date_input = st.date_input("Man Date", max_date, min_value=min_date, max_value=max_date)
