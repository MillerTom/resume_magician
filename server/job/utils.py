import requests
import json
from django.conf import settings

def execute_gviz_query(query):
    SHEET_ID = settings.SPREAD_SHEET_ID
    WORKSHEET_ID = settings.SHEET_ID
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?"
    params = { 'tq': query, 'tqx': 'out:json', 'gid': WORKSHEET_ID }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        raw_data = response.text.lstrip("/*O_o*/\ngoogle.visualization.Query.setResponse(").rstrip(");")
        data = json.loads(raw_data)
        return data

    except Exception as e:
        print(f"Error executing gViz query: {e}")
        return None