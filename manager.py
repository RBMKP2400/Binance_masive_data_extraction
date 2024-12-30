import json
import os

def create_config(symbol, interval=None, timezone ='Europe/Madrid', start_date=None, end_date=None, days_range = None, index=None):
    config = {
        "symbol": symbol,
        "interval": interval,
        "timezone": timezone,
        "start_date": start_date,
        "end_date": end_date,
        "days_range": days_range,
        "output_path": f"/output/"
    }

    config_path = os.getcwd() + f"/config/config_{index}.json"
    with open(config_path, 'w') as f:
        json.dump(config, f)
    print(f"Creada configuración: {config_path}")

#############################################################################
# USUARIO: CREA TANTAS CONFIGURACIONES COMO DOCKERS DESEES GENERAR
#############################################################################

create_config("BTCUSDT", "1m", start_date="01-01-2024", index = 1)
create_config("BTCUSDT", "1m", start_date="01-01-2023", end_date="31-12-2023", index = 2)
create_config("BTCUSDT", "1m", start_date="01-01-2022", end_date="31-12-2022", index = 3)
create_config("BTCUSDT", "1m", start_date="01-01-2021", end_date="31-12-2021", index = 4)
create_config("BTCUSDT", "1m", start_date="01-01-2020", end_date="31-12-2020", index = 5)

#############################################################################

config_docs = [f for f in os.listdir('./config')]

dockercompose_text = """
version: "3.9"
services:
"""
for i, name in enumerate(config_docs):
    text = f"""
      extractor_{i}:
        build:
          context: ./app
          dockerfile: Dockerfile
        environment:
          - CONFIG_PATH=/config/{name}
        volumes:
          - ./config:/config
          - ./output:/output
    """
    dockercompose_text += text

filename = f'docker-compose.yml'
with open(filename, 'w') as f:
    f.write(dockercompose_text)

print("Se ha creado el archivo 'docker-compose.yml'")