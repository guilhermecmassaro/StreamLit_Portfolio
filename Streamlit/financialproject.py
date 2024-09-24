import streamlit as st
import pandas as pd
from functions import *
import altair as alt
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
firstline_col1, firstline_col2, firstline_col3 = st.columns([1,2,2], gap="large",vertical_alignment="top")

with firstline_col1:

    col1, col2 = st.columns(2, gap="medium",vertical_alignment="top")

    # Lista de opções de ativos
    assets_options = ['PETR4.SA', 'ITUB4.SA', 'BBDC4.SA']

    # Filtro de seleção do ativo
    with col1:
        asset_filter = st.radio("Pick a Asset!", options=assets_options, key='asset')
        st.write(f"You selected: {asset_filter}")

    with col2:
        # Configuração das datas
        max_date = datetime.now()
        min_date = max_date - timedelta(days=365 * 5)

        min_date_input = st.date_input("Min Date", min_date, min_value=min_date, max_value=max_date)
        max_date_input = st.date_input("Max Date", max_date, min_value=min_date, max_value=max_date)

        min_date_input = pd.to_datetime(min_date_input)
        max_date_input = pd.to_datetime(max_date_input)

    st.write('### Who made this app?')
    linkedin_link = 'https://www.linkedin.com/in/guilhermecmassaro/'
    github_link = 'https://github.com/guilhermecmassaro'
    resume_link = 'https://1drv.ms/b/s!ApgvMVoVyIBziqgHWeJCcu_TinrcNw?e=OALAAc'

    # Dividindo os botões em colunas
    col1, col2, col3= st.columns([1,1,1], gap="small",vertical_alignment="center")

    with col1:
        st.link_button("GitHub",url = github_link, type = 'primary')

    with col2:
        st.link_button("Resume", url = resume_link, type = 'primary')
    
    with col3:
        st.link_button("LinkedIn", url = linkedin_link, type = 'primary')

# Verifica se os dados do ativo já estão armazenados no session_state
if asset_filter not in st.session_state:
    load_data(asset_filter=asset_filter)  # Faz o download dos dados apenas se não existirem

# Filtra os dados de acordo com o intervalo de datas selecionado
df_filtered = st.session_state[asset_filter][(st.session_state[asset_filter]['Date'] >= min_date_input) & (st.session_state[asset_filter]['Date'] <= max_date_input)]
df_filtered = df_filtered.reset_index(drop=True) # Ignorando o indice

first_line = df_filtered['Adj Close'].iloc[0] # Criando uma variável para a primeira linha da tabela
df_filtered['Normalized Adj Close'] = df_filtered['Adj Close']/first_line # Criando uma coluna normalizada para acompanhar a evolução

with firstline_col2:
    # Gráfico de Adj Close
    st.write(f'### Data historical of {asset_filter}')
    st.line_chart(data = df_filtered, x = 'Date', y = 'Adj Close',width = 1000, height = 300)

with firstline_col3:
    # Gráfico de Normalization Adj Close
    st.write(f'### Normalized evolution of {asset_filter}')
    st.line_chart(data = df_filtered, x = 'Date', y = 'Normalized Adj Close', width = 1000, height = 300)

# Gráfico de Log Return
st.write(f'### Daily logarithmic returns of {asset_filter}')
st.bar_chart(data = df_filtered, x = 'Date', y = 'Log Return', width = 1000, height = 500)

secondline_col1, secondline_col2 = st.columns([1,2], gap="large",vertical_alignment="top")

with secondline_col1:
    # Forms de simulação
    st.write(f'### Simulation from {min_date.date()} to {max_date.date()} of {asset_filter}')
    forms = st.form(key = 'simulation_form', clear_on_submit = False)
    with forms:
        numbers_invested_input = st.number_input(label = 'Amount invested', min_value = 0.0, step = 100.0, value = 1000.0)
        ir_toggle = st.toggle("IR Mode")
        inflation_toggle = st.toggle("Inflation Mode")
        st.form_submit_button(label = 'Submit', on_click=simulation_calculator_ir(asset_df=df_filtered,investment=numbers_invested_input))

with secondline_col2:
    # Download do CSV filtrado
    st.write('### Feel Free to export the data as CSV')
    st.download_button('Download CSV', df_filtered.to_csv(), 'data.csv', 'text/csv', key='download-csv')
    st.dataframe(df_filtered)





