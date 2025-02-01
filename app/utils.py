import pandas as pd
from datetime import datetime, timedelta
import pytz
import json
import requests
from tqdm import tqdm


class Lib():
    def __init__(self, symbol, timezone='Europe/Madrid', bar_size_setting='1m', start_date=None, end_date=None,  duration=None):
        self.symbol = symbol
        self.timezone = timezone
        self.bars = bar_size_setting
        self.chucks = self.chucks(start_date, end_date, duration)
        #self.monthly_chunks = self.monthly_chunks(self.chucks)

    def chucks(self, start_date=None, end_date=None,  duration=None):
        # Convertimos los inputs a mayúsculas y preparamos la zona horaria
        timezone = pytz.timezone(self.timezone)
        # Si no se han definido las fechas, las calculamos
        if end_date is None:
            end_date = datetime.now(tz=timezone)
        else:
            end_date = end_date.split("-")
            end_date = timezone.localize(datetime(int(end_date[2]), int(end_date[1]), int(end_date[0]), 23, 59))

        if start_date is None:
            start_date = end_date - timedelta(days=duration or 1)
        else:
            start_date = start_date.split("-")
            start_date = timezone.localize(datetime(int(start_date[2]), int(start_date[1]), int(start_date[0]), 00, 00))

        # Dividir en chunks de 1000 minutos
        chunk_size = 1000
        chunks = []
        current_start = start_date

        while current_start < end_date:
            if self.bars[-1] == 'm':
                current_end = current_start + timedelta(minutes=chunk_size)
            elif self.bars[-1] == 'h':
                current_end = current_start + timedelta(hours=chunk_size)
            elif self.bars[-1] == 'd':
                current_end = current_start + timedelta(days=chunk_size)
            elif self.bars[-1] == 'w':
                current_end = current_start + timedelta(weeks=chunk_size)
            elif self.bars[-1] == 's':
                current_end = current_start + timedelta(seconds=chunk_size)
            else:
                current_end = end_date

            if current_end > end_date:
                current_end = end_date

            chunks.append((current_start, current_end))
            current_start = current_end
        return chunks

    def historical_data(self, chucks):

        timezone = pytz.timezone(self.timezone)
        df = pd.DataFrame()

        # Extraer datos para cada chunk con barra de progreso
        for value in tqdm(chucks, desc="Obteniendo datos históricos"):
            start = value[0]
            end = value[1]
            # Convertimos las fechas a UTC
            start_date = start.astimezone(pytz.UTC)
            end_date = end.astimezone(pytz.UTC)

            # Convertimos las fechas a timestamps para la API de Binance
            start_timestamp = int(start_date.timestamp() * 1000)
            end_timestamp = int(end_date.timestamp() * 1000)

            # Preparamos la consulta a la API de Binance
            url = 'https://api.binance.com/api/v3/klines'

            params = {
                "symbol": self.symbol,
                "interval": self.bars,
                "startTime": start_timestamp,
                "endTime": end_timestamp,
                "limit": 1000
            }

            # Obtenemos los datos y los convertimos en un DataFrame
            data_df = pd.DataFrame(
                json.loads(requests.get(url, params=params).text),
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
                         'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
            )

            # Filtramos las columnas necesarias y actualizamos start_date
            data_df = data_df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

            # Concatenamos los datos obtenidos al DataFrame principal
            df = pd.concat([df, data_df], ignore_index=True)

        # Ajustamos los tipos de datos y la zona horaria
        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(timezone)

        df['year'] = df['timestamp'].dt.year
        df['month'] = df['timestamp'].dt.month
        df['day'] = df['timestamp'].dt.day
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute

        return df