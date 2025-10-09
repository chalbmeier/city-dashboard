# Dashboard: Quality of Life in European Cities (2023)

An interactive **Python/Dash** dashboard to present data from the *Quality of Life in European Cities* survey. 

The dashboard is running with Google Cloud Run at https://citydashboard-557114830893.europe-west1.run.app/. The server may take a few seconds to start up when idle (cold start).


## Project description
This learning project helped me understand how to build browser-based dashboards with Python Dash. The layout is not perfect, and the code includes little documentation since the project is not intended to be maintained. Still, it served me well for understanding Dash callbacks and their interaction with JavaScript and CSS. 

## Data source
The dashboard uses data from the *Quality of Life in European Cities* survey conducted by the European Commission / DG Regional and Urban Policy in 2023. The target population was residents aged 15+ in the cities of interest.

The survey used a stratified random sample. The statistics shown are based on approximately 850 completed interviews per city,e reweighted to match population totals. In line with the official reports, for each indicator the “don’t know/not answered” category is excluded and the remaining categories are rescaled so percentages refer to respondents who provided a valid answer.

The data and official reports are available at https://ec.europa.eu/regional_policy/information-sources/maps/quality-of-life_en

I’m not affiliated with the European Commission.


## Main Python packages
- dash
- dash-iconify
- dash-leaflet
- pandas 
- plotly

## Run locally 
If you would like to run the dashboard locally, follow these steps:

```bash
# 1) Clone repo
git clone https://github.com/chalbmeier/city-dashboard.git
cd city-dashboard

# 2) Create environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install
pip install -U pip
pip install -r requirements.txt

# 4) Run
python run.py
```

## Credits
- © OpenStreetMap contributors.
- European Commission / DG REGIO - Quality of Life in European Cities (2023).
