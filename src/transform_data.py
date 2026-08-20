import pandas as pd
from pathlib import Path
import json

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'
columns_names_to_drop = ['weather', 'weather_icon', 'sys.type']

def create_dataframe(path_name:str) -> pd.DataFrame:
    logging.info("-> Criando DataFrame do arquivo JSON...")
    path = path_name

    if not path.exits():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    logging.info(f"\n -> DataFrame criado com {len(df)} linha(s)")
    return df

def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, df_weather], axis=1)
    logging.info(f"\n✓ Coluna 'weather' normalizada - {len(df.columns)} colunas")


    return df


def drop_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    logging.info(f"\n→ Removendo colunas: {columns_names}")
    df = df.drop(columns=columns_names)
    logging.info(f"✓ Colunas removidas - {len(df.columns)} colunas restantes")
    return df 


