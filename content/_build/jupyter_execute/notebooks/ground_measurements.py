# Ground measured solar radiation data

## Major radiation station networks

* Baseline Surface Radiation Network
* SURFRAD
* SOLRAD








## Baseline Surface Radiation Network (BSRN)

import folium
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None)

bsrn_url = 'https://wiki.pangaea.de/wiki/BSRN#Sortable_Table_of_Stations'
bsrn_stations = pd.read_html(bsrn_url, index_col=1)[0]
bsrn_stations

bsrn_stations.style

# Initialize Folium map
m = folium.Map(
    location=[0, 15],
    zoom_start=1,
    min_zoom=1,
    max_bounds=True,
    tiles='openstreetmap',
    )

# Add each station to the map
for index, row in bsrn_stations.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Station full name']} ({row.name})",
        icon=folium.Icon(color='blue')
    ).add_to(m)

m  # Show the map

## SURFRAD and SOLRAD

def convert_latitude_longitude(l):
    """Function to convert from latitude/longitude string
    to float with sign convention of ISO 19115"""
    l = l.replace(' ', '')  # Remove all spaces
    cardinal_signs = {'N': 1, 'S': -1, 'E': 1, 'W': -1}
    for c in cardinal_signs.keys():
        if c in l:
            return cardinal_signs[c]*float(l.replace(c, '').replace('°', ''))

surfrad_url = 'https://www.esrl.noaa.gov/gmd/grad/surfrad/sitepage.html'
surfrad_stations = pd.read_html(surfrad_url, index_col=0)[0].iloc[:-1]
surfrad_stations[['Latitude', 'Longitude']] = surfrad_stations[['Latitude', 'Longitude']].applymap(convert_latitude_longitude)
surfrad_stations

solrad_url = 'https://www.esrl.noaa.gov/gmd/grad/solrad/solradsites.html'
solrad_stations = pd.read_html(solrad_url, index_col=0)[0]
solrad_stations.loc['STE',['Name','Latitude','Longitude']] = ['Sterling, Virginia', '38.97203° N', '77.48690° W']
solrad_stations[['Latitude', 'Longitude']] = \
    solrad_stations[['Latitude', 'Longitude']].applymap(convert_latitude_longitude)
solrad_stations

### Initialize Folium map
m = folium.Map(
    location=[40, -95],
    zoom_start=4,
    min_zoom=2,
    max_bounds=True,
    tiles='OpenStreetMap',
)

# Add stations to the map
for i, stations in enumerate([surfrad_stations, solrad_stations]):
    for index, row in stations.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Name']} ({row.name})",
            icon=folium.Icon(color=['blue', 'red'][i])
            ).add_to(m)

# Add Category Legend
legend_html = """
<div style="position:fixed;
     bottom: 50px; 
     left: 50px; 
     width: 120px; 
     height: 85px; 
     border:2px solid grey; 
     z-index: 9999;
     font-size:14px;">
     &nbsp;<b>Station network:</b><br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:blue"></i>&nbsp;SURFRAD<br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:red"></i>&nbsp;SOLRAD<br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:orange"></i>&nbsp;SRML<br>
</div>"""

m.get_root().html.add_child(folium.Element(legend_html))  # Add Legend

m.add_child(folium.LatLngPopup())  # Show latitude,longitude when clicking
m  # Show map





