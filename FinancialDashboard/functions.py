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
    
# Função para carregar os dados do ativo e armazenar no st.session_state
def load_data(asset_filter):
    asset = FinancialData(asset_filter)
    df_asset = asset.get_historical_data().reset_index().round(3)
    df_asset['Date'] = pd.to_datetime(df_asset['Date'])
    st.session_state[asset_filter] = df_asset  # Armazena o dataframe no session_state 

def average_log_return_calculator(asset_df):
    total_days_of_open_market = asset_df['Date'].count()
    daily_average_log_return = asset_df['Log Return'].mean()
    average_log_return = total_days_of_open_market * daily_average_log_return
    return average_log_return

def simulation_calculator_ir(asset_df, investment):
    initial_number = investment
    average_log_return = average_log_return_calculator(asset_df)
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
                                 index=[0])
    df_simulator = df_simulator.T
    df_simulator.columns = ['Simulator']
    return df_simulator

def simulation_calculator(asset_df, investment):
    initial_number = investment
    average_log_return = average_log_return_calculator(asset_df)
    final_number = (initial_number * (1 + average_log_return)).round(2)
    average_return = (average_log_return * 100).round(2)
    gross_profit = (final_number - initial_number).round(2)

    df_simulator = pd.DataFrame({'Initial Investment': initial_number,
                                 'Average Return': f'{average_return} %', 
                                 'Gross Revenue' : final_number,
                                 'Gross Profit': gross_profit}, 
                                 index=[0])
    df_simulator = df_simulator.T
    df_simulator.columns = ['Simulator']
    return df_simulator
    
def standard_deviation_calculator(asset_df):
    total_days_of_open_market = asset_df['Date'].count()
    daily_average_log_std= asset_df['Log Return'].std()
    std_deviation = total_days_of_open_market * daily_average_log_std
    return std_deviation

def beta_calculator(asset_df, market_df):
    # Cálculo da covariância entre os retornos do ativo e do índice
    covariance = np.cov(asset_df['Log Return'][1:], market_df['Log Return'][1:])[0, 1]
    # Cálculo da variância dos retornos do mercado
    variance_market = market_df['Log Return'][1:].var()
    # Cálculo do Beta
    beta = (covariance / variance_market).round(3)
    return beta


def sharpe_ratio_calculator(asset_df, risk_free_rate):
    # Cálculo da média do retorno logarítmico
    mean_return = asset_df['Log Return'].mean()
    # Cálculo do desvio padrão do retorno logarítmico
    std_deviation = asset_df['Log Return'].std()
    # Cálculo do Sharpe Ratio
    sharpe_ratio = ((mean_return - risk_free_rate) / std_deviation).round(3)
    return sharpe_ratio



