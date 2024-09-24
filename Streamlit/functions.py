import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

class FinancialData:

    def __init__(self, ticker):
        self.ticker = ticker

    def get_historical_data(self):
        ticker = self.ticker
        data = yf.download(ticker)
        data ['Log Return'] = np.log(data['Adj Close']/(data['Adj Close']).shift(1)) # Criando uma coluna de retorno logarítmico diário
        data['Asset'] = self.ticker # Adicionando uma coluna para o nome do ativo
        return data
    
def simulation_calculator_ir(asset_df, investment):
    initial_number = investment
    total_days_of_open_market = asset_df['Date'].count()
    daily_average_log_return = asset_df['Log Return'].mean()
    average_log_return = total_days_of_open_market * daily_average_log_return
    final_number = (initial_number * (1 + average_log_return)).round(2)
    ir = 0.15
    average_return = (average_log_return * 100).round(2)
    gross_profit = (final_number - initial_number).round(2)
    interest_rate = 0.15 * 100
    net_profit = (gross_profit * (1 -ir)).round(2)

    df_simulator = pd.DataFrame({'Initial Investment' : initial_number,
                                 'Average Return': f'{average_return} %', 
                                 'Gross Revenue' : final_number,
                                 'Gross Profit': gross_profit, 
                                 'Interest rate': f'{interest_rate} %',
                                 'Net Profit': f'{net_profit}'},
                                 index=[0], columns = ['Simulator'])
    st.dataframe(df_simulator.T)
    #st.write(f'Average Return: {average_log_return*100:.2f} %')
    #st.write(f'Gross Profit: {final_number:.2f}')
    #st.write(f'Interest rate: {ir*100:.2f} %')
    #st.write(f'Net Profit: {(final_number - initial_number) * (1 -ir):.2f}')

def simulation_calculator(asset_df, investment):
    initial_number = investment
    total_days_of_open_market = asset_df['Date'].count()
    daily_average_log_return = asset_df['Log Return'].mean()
    average_log_return = total_days_of_open_market * daily_average_log_return
    final_number = (initial_number * (1 + average_log_return)).round(2)
    average_return = (average_log_return * 100).round(2)
    gross_profit = (final_number - initial_number).round(2)

    df_simulator = pd.DataFrame({'Initial Investment': initial_number,
                                 'Average Return': f'{average_return} %', 
                                 'Gross Revenue' : final_number,
                                 'Gross Profit': gross_profit}, 
                                 index=[0], columns= 'Simulator')
    st.dataframe(df_simulator.T)
    #st.write(f'Average Return: {average_log_return*100:.2f} %')
    #st.write(f'Gross Revenue: {final_number:.2f}')
    #st.write(f'Gross Profit: {(final_number - initial_number):.2f}')
# Função para carregar os dados do ativo e armazenar no st.session_state
def load_data(asset_filter):
    asset = FinancialData(asset_filter)
    df_asset = asset.get_historical_data().reset_index().round(3)
    df_asset['Date'] = pd.to_datetime(df_asset['Date'])
    st.session_state[asset_filter] = df_asset  # Armazena o dataframe no session_state
    