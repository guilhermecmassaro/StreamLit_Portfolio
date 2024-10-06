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
        # data ['Log Return'] = np.log(data['Adj Close']/(data['Adj Close']).shift(1)) # Criando uma coluna de retorno logarítmico diário
        data['Log Return'] = data['Adj Close'].pct_change()
        data['Asset'] = self.ticker # Adicionando uma coluna para o nome do ativo
        return data

    def market_capitalization(self, df_asset):
        ticker = self.ticker
        marketCap = df_asset['Adj Close'][-1] * yf.Ticker(ticker).info['sharesOutstanding']      

    def price_to_earnings_ratio(self, df_asset):
        ticker = self.ticker
        peRatio = df_asset['Adj Close'][-1] / yf.Ticker(ticker).info['epsTrailingTwelveMonths'] 
    
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

def df_groupby_monthly(asset_df):
    df = asset_df
    df['Year'] = df['Date'].apply(lambda x: x.year)
    df['Month'] = df['Date'].apply(lambda x: x.month)
    df['Month/Year'] = df['Date'].apply(lambda x: x.strftime('%m/%Y'))
    df = df[['Month/Year','Year','Month','Asset', 'Log Return','Adj Close']]
    df_grouped = df.groupby(['Month/Year','Year', 'Month','Asset']).agg({'Log Return': ['sum','std'], 'Adj Close': ['min','max','mean']}).reset_index()
    df_grouped.set_index('Month/Year', inplace=True)
    df_grouped = df_grouped.sort_values(by=['Year','Month'], ascending=True)
    df_grouped = df_grouped[['Log Return','Adj Close']]
    df_grouped.columns = ['Average Return','Average Return Std' ,'Min Adj Close','Max Adj Close','Average Adj Close']   

    df_grouped['Average Return'] = df_grouped['Average Return'].apply(lambda x: f'{(x*100):.2f} %')
    df_grouped['Average Return Std'] = df_grouped['Average Return Std'].apply(lambda x: f'{(x*100):.2f} %')
    df_grouped['Average Adj Close'] = df_grouped['Average Adj Close'].round(2)
    df_grouped['Min Adj Close'] = df_grouped['Min Adj Close'].round(2)
    df_grouped['Max Adj Close'] = df_grouped['Max Adj Close'].round(2)

    return df_grouped

