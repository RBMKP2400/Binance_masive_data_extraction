import utils as ut
import os
import json

# Leer parámetros
config_path = os.getenv("CONFIG_PATH", os.getcwd()[:-4] + f"/config/config_0.json")

with open(config_path, 'r') as f:
    config = json.load(f)

symbol = config.get("symbol")
timezone = config.get("timezone", None)
bar_size_setting = config.get("interval", None)
start_date = config.get("start_date", None)
end_date = config.get("end_date", None)
duration = config.get("days_range", None)
output_path = config.get("output_path", os.getcwd()[:-4] + f"/output/")
#output_path = os.getcwd()[:-4] + f"/output/"

lib_instance = ut.Lib(symbol, timezone, bar_size_setting, start_date, end_date, duration)
df = lib_instance.historical_data(lib_instance.chucks)

unique_year_months = df[['year', 'month']].drop_duplicates().to_numpy()
for year, month in unique_year_months:
    key = f"{year}_{month:02d}.parquet"
    file_path = os.path.join(output_path, f"{symbol}_{bar_size_setting}_{key}.parquet")

    df_filtered = df[(df['year'] == year) & (df['month'] == month)]
    df_filtered.to_parquet(file_path, index=False)
    print(f"Datos guardados en {file_path}")

print(f"Extracción de datos para {symbol} desde {start_date} hasta {end_date} completada.")

