# Historical Massive Data Extractor for Binance

This repository enables users to extract historical data at intervals of up to 1 second using the Binance API without the need for an account on the platform. Additionally, by utilizing Docker Compose, the program can extract information in parallel, significantly reducing extraction times.

Your data will be saved in the output file, so feel free to clear the data in this file as you wish.

## Step 1: Create Configuration Files and `docker-compose.yml`

1. Navigate to `manager.py` and create as many configurations as needed for the Docker containers.

**Notes:** The `create_config` dictionary indicates the input values needed to query the Binance API for data, so the format is essential:

### Parameters:
- **Symbol**: Specify the symbol you want to retrieve.
- **Interval**: This defines the bar size of the candle, following the API options. Supported kline intervals (case-sensitive) include:
    - **Seconds**: 1s
    - **Minutes**: 1m, 3m, 5m, 15m, 30m
    - **Hours**: 1h, 2h, 4h, 6h, 8h, 12h
    - **Days**: 1d, 3d
    - **Weeks**: 1w
    - **Months**: 1M 
- **days_range**: Duration in days to obtain historical data (if not specified, calculated from the dates).
- **start_date**: Start date in the format: "dd-mm-yyyy".
- **end_date**: End date (optional) in the format: "dd-mm-yyyy".
- **timezone**: Timezone for adjusting the data.
- **index**: Define the index of the config file. Every index must be diferent.

## Step 2: Start Your Docker Containers

To run your Docker containers using Docker Compose, follow these steps:

1. **Open Docker Desktop**: If you're on Windows, ensure Docker Desktop is running.
2. **Navigate to your project directory**: Open your terminal and change the directory to where your `docker-compose.yml` file is located. You can do this using the `cd` command:
   ```bash
   cd path/to/your/project
3. Run Docker Compose: Execute the following command to build and start your containers:
   ```bash
   docker-compose up
