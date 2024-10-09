# import
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# import variaveis de ambiente
load_dotenv()

commodities = ['CL=F', 'GC=F', 'SI=F']

DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

# pegar cotacao dos ativos
def buscar_dados_commodities(simbolo, periodo='5d', intervalo='1d'):
    ticker = yf.Ticker(simbolo) # ao invés de usar um response, a biblioteca yf tem o método ticker que retornará a cotação desejada
    dados = ticker.history(period=periodo, interval= intervalo)[['Close']] # ira retornar um dataframe apenas com a coluna 'Close', se quiser pegar cotações de hora em hora, basta tirar o 'Close'.
    dados['simbolo'] = simbolo # criar uma coluna nova ['simbolo'] onde ele irá receber o prório simbolo do parametro da função, para retornar o ticker consultado
    return dados

# concatenar os ativos
def buscar_todos_dados_commodities(commodities):
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados) #para cada dado retornado do dataset irá ser passado o simbolo 
    return pd.concat (todos_dados) #retornar e concatenar os dados

# salvar no banco de dados
def salvar_no_postgres(df, schema='public'):
    df.to_sql('commodities', engine, if_exists='replace', index=True, index_label = 'Date', schema=schema)


if __name__ == '__main__':
    dados_concatenados = buscar_todos_dados_commodities(commodities)
    salvar_no_postgres(dados_concatenados, schema='public')

