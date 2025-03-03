import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

list_tickers = ['ITUB3.SA', 'BBDC3.SA', 'BBAS3.SA', '^BVSP', 'SANB11.SA']

def carregar_dados(ticker, inicio, fim):
    #Baixar os dados do ticker
    import yfinance as yf
    # df = yf.download(ticker ,start=f'{str(ano)}-01-01')
    df = yf.download(ticker, start=f'{inicio}-01-01', end=f'{fim}-12-31')
    print(f'Dados de {ticker} carregados com sucesso!')
    return df

def tratar_dados(df, periodo):
    df.reset_index(inplace=True)

    # Garantir que as colunas não tenham MultiIndex
    df.columns = df.columns.get_level_values(0)

    # Converter a coluna 'Date' para o formato de data
    df['Date'] = pd.to_datetime(df['Date'])

    if periodo == 'ano_mes':
        # Criar a coluna 'Ano-Mês' no formato YYYYMM
        col = 'ano_mes'
        dt_format = '%Y%m'    
    elif periodo == 'ano':
        # Criar a coluna 'Ano' no formato YYYY
        col = 'ano'
        dt_format = '%Y'
        
    df[col] = df['Date'].dt.strftime(dt_format)
    df = df.groupby(col).agg({'Close':'mean'}).reset_index() 

    #Calcular o Retorno Logarítmico
    df['log_return'] = (np.log(df['Close'] / df['Close'].shift(1))) * 100

    return df