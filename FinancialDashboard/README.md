# Financial Data Dashboard

This project is a financial dashboard built using **Streamlit**. It allows users to view historical data and perform simulations on stock data from selected assets. The dashboard displays a variety of interactive charts and provides data export options, along with simulation features that take into account different investment scenarios.

## Features

- **Asset Selection**: Choose between different assets to analyze.
- **Date Range Filter**: Select a date range to filter the historical data.
- **Historical Data**: View historical adjusted closing prices for the selected asset.
- **Normalized Data Visualization**: Display a normalized view of asset performance over time.
- **Daily Logarithmic Returns**: Visualize daily log returns with color-coded bars.
- **Investment Simulation**: Perform investment simulations with or without Income Tax (IR) Mode.
- **CSV Export**: Download filtered data as a CSV file.
- **Responsive Layout**: The dashboard is laid out using columns to make efficient use of screen space.

## Installation

To run this project, you'll need Python installed and the following Python packages:

```bash
pip install streamlit pandas altair
```

Additionally, ensure that you have the following functions available in a functions.py file or another module that you import in your script:

1. **load_data()**: Function to fetch the asset data.
2. **simulation_calculator()**: Function to perform the simulation calculations.
3. **simulation_calculator_ir()**: Function for the simulation in IR mode.

## Running the Application
To run the Streamlit application, execute the following command in your terminal:

```bash
streamlit run financialproject.py
```

Make sure that your_script.py is the name of the Python file containing the above code.

## Usage

1. **Select an Asset**: Use the radio buttons to select an asset (PETR4.SA, ITUB4.SA, or BBDC4.SA).
2. **Set Date Range**: Use the date inputs to select the range of dates you want to analyze.
3. **View Data and Charts**: The application will display the asset's historical data and normalized performance over time.
4. **Log Return Visualization**: You can also view the daily logarithmic returns in a color-coded bar chart (green for positive returns, red for negative returns).
5. **Investment Simulation**: You can input an investment amount and toggle the IR Mode to simulate different investment scenarios.
6. **Download Data**: Filtered data can be downloaded in CSV format.

## Project Structure

```bash
├── README.md            # Project overview and instructions
├── financialproject.py  # Main Python script with Streamlit code
├── functions.py         # Helper functions (load_data, simulation_calculator, etc.)
├── requirements.txt     # Required Python packages
```

## Dashboard Layout

- **First Section**:
    - Asset selection and date range filtering.
    - Historical and normalized adjusted close price charts.
      
- **Second Section**:
   - Color-coded bar chart of daily log returns.
     
- **Third Section**:
   - Investment simulation form with Income Tax (IR) mode.
   - CSV export option.
