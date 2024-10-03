import streamlit as st
import pandas as pd
from functions import *
import altair as alt
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
firstline_col1, firstline_col2, firstline_col3 = st.columns([1,2,2], gap="large",vertical_alignment="top")
secondline_col1, secondline_col2 = st.columns([1.2,3], gap="large",vertical_alignment="top")
thirdline_col1, thirdline_col2 = st.columns([1,2], gap="large",vertical_alignment="top")

# Lista de opções de ativos
assets_options = ['PETR4.SA', 'ITUB4.SA', 'BBDC4.SA']

with firstline_col1:

    col1, col2 = st.columns(2, gap="medium",vertical_alignment="top")

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
if 'IBOV' not in st.session_state:
    load_data(asset_filter='^BVSP')  # Código do Ibovespa para yfinance

if asset_filter not in st.session_state:
    load_data(asset_filter=asset_filter)  # Faz o download dos dados apenas se não existirem

# Filtra os dados de acordo com o intervalo de datas selecionado
df_asset_filtered = st.session_state[asset_filter][(st.session_state[asset_filter]['Date'] >= min_date_input) & (st.session_state[asset_filter]['Date'] <= max_date_input)]
df_asset_filtered = df_asset_filtered.reset_index(drop=True) # Ignorando o indice
first_line = df_asset_filtered['Adj Close'].iloc[0] # Criando uma variável para a primeira linha da tabela
df_asset_filtered['Normalized Adj Close'] = df_asset_filtered['Adj Close']/first_line # Criando uma coluna normalizada para acompanhar a evolução

df_market_filtered = st.session_state['^BVSP'][(st.session_state['^BVSP']['Date'] >= min_date_input) & (st.session_state['^BVSP']['Date'] <= max_date_input)]
df_market_filtered = df_market_filtered.reset_index(drop=True)

df_asset_filtered_grouped = df_groupby_monthly(df_asset_filtered)
df_market_filtered_grouped = df_groupby_monthly(df_market_filtered)


with firstline_col2:
    # Gráfico de Adj Close
    st.write(f'### Data Historical ({asset_filter})')
    st.line_chart(data = df_asset_filtered, x = 'Date', y = 'Adj Close',width = 1000, height = 300)

with firstline_col3:
    # Gráfico de Normalization Adj Close
    st.write(f'### Normalized Evolution ({asset_filter})')
    st.line_chart(data = df_asset_filtered, x = 'Date', y = 'Normalized Adj Close', width = 1000, height = 300)

with secondline_col1:
    
    st.write(f'### Quick Statistical Analysis ({asset_filter})')
    st.dataframe(df_asset_filtered_grouped.T, use_container_width=True)

with secondline_col2:

    # Sample DataFrame (df_asset_filtered should already exist in your case)
    df_asset_filtered['Color'] = df_asset_filtered['Log Return'].apply(lambda x: 'green' if x > 0 else 'red')

    # Define the Altair chart
    log_return_chart = (
        alt.Chart(df_asset_filtered)
        .mark_bar()
        .encode(
            x='Date:T',  # 'Date:T' ensures it's treated as a temporal field
            y='Log Return:Q',
            color=alt.condition(
                alt.datum['Log Return'] > 0,  # condition for positive values
                alt.value('green'),           # color for positive values
                alt.value('red')              # color for negative values
            )
        )
        .properties(width=1000, height=500)
    )

    # Display the Altair chart in Streamlit
    st.write(f'### Daily Logarithmic Returns ({asset_filter})')
    st.altair_chart(log_return_chart, use_container_width=True)

with thirdline_col1:
    st.write(f'### Simulation From {min_date_input.date()} to {max_date_input.date()} ({asset_filter})')
            
    # Create the form
    with st.form(key='simulation_form', clear_on_submit=False):

        with st.expander('Read me first!'):
            st.write('''This is a quick and simple simulation!
                     We don\'t take into account inflation, contributions and dividends. 
                     Please, check your results carefully!''')

        # Inputs inside the form
        numbers_invested_input = st.number_input(label='Amount invested', min_value=0.0, step=100.0, value=1000.0)
        ir_toggle = st.toggle("IR Mode")
        
        # Submit button
        submit_button = st.form_submit_button(label='Submit')

        # Execute only when the form is submitted
        if submit_button:
            if ir_toggle:
                # Replace the dataframe with the one from IR Mode
                df_to_display = st.dataframe(simulation_calculator_ir(asset_df=df_asset_filtered, investment=numbers_invested_input), use_container_width=True)
            else:
                # Normal dataframe without IR mode
                df_to_display = st.dataframe(simulation_calculator(asset_df=df_asset_filtered, investment=numbers_invested_input), use_container_width=True)

with thirdline_col2:
    # Download do CSV filtrado
    st.write('### Feel Free to export the data as CSV')
    df_asset_filtered['Date'] = df_asset_filtered['Date'].apply(lambda x: x.date())
    df_asset_filtered.drop(columns = ['Color'], axis = 1, inplace = True)
    st.download_button('Download CSV', df_asset_filtered.to_csv(), 'data.csv', 'text/csv', key='download-csv')
    st.dataframe(df_asset_filtered, use_container_width=True,hide_index= True)





