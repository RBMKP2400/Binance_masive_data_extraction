import utils as ut
import os
import json

# Leer parámetros
config_path = os.getenv("CONFIG_PATH", "/config/config_1.json")
# config_path = os.getcwd()[:-4] + "/config/config_2.json"
with open(config_path, 'r') as f:
    config = json.load(f)

symbol = config.get("symbol")
timezone = config.get("timezone", None)
bar_size_setting = config.get("interval", None)
start_date = config.get("start_date", None)
end_date = config.get("end_date", None)
duration = config.get("days_range", None)
output_path = config.get("output_path", "/output")


lib_instance = ut.Lib(symbol, timezone, bar_size_setting, start_date, end_date, duration)
monthly_chunks = lib_instance.monthly_chunks

for key, value in monthly_chunks.items():
    df = lib_instance.historical_data(value)
    file_path = os.path.join(output_path, f"{symbol}_{bar_size_setting}_{key}.parquet")
    df.to_parquet(file_path, index=False)
    print(f"Datos guardados en {file_path}")

print(f"Extracción de datos para {symbol} desde {start_date} hasta {end_date} completada.")

