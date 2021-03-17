# Ground-based solar irradiance data

Conducted ground-based solar irradiance measurements is useful for obtaining information on the local solar resource, but also extremely for determining the accuracy of sattelite and reanalysis solar irradiance methods and validating solar radiation models.

In this section, the major ground-based solar radiation monitoring network will be introduced and it will be demonstrated how data can be obtained from these sources.

## Major radiation station networks

There exists a number of ground-based solar radiation monitoring networks, of which most are operated by national weather services or research organizations:

* [Baseline Surface Radiation Network - BSRN (global)](https://bsrn.awi.de/)
* [SURFRAD by NOAA (US)](https://www.esrl.noaa.gov/gmd/grad/surfrad/)
* [SOLRAD by NOAA (US)](https://www.esrl.noaa.gov/gmd/grad/solrad/)
* [ESMAP - World Bank ](https://globalsolaratlas.info/solar-measurement)
* [SRML by the University of Oregon (Northwestern US)](http://solardat.uoregon.edu/index.html)
* [NREL (US)](https://midcdmz.nrel.gov/)
* Enermena
* SMHI (Sweden)
* BoM (Australia)
* SAURAN (South Africa)
* MeteoSwiss (Switzerland)

import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None)

## Baseline Surface Radiation Network (BSRN)

Of the monitoring networks listed above, the Baseline Surface Radiation Network (BSRN) stands out, as the only monitoring network with global coverage. 


bsrn_url = 'https://wiki.pangaea.de/wiki/BSRN#Sortable_Table_of_Stations'
bsrn_stations = pd.read_html(bsrn_url, index_col=1)[0]
bsrn_stations

To visualize the geographical coverage of the BSRN, it is helpful to plot the stations on map. This can easily be achieved using the Folium library in Python, which generates an interactive map. This is especially useful when trying to locate the nearest BSRN station to a point of interest or get an overview of the coverage in a particular region.

import folium

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

The distribution of the BSRN stations is clearly shown in the map above, with some regions having a high concentration of stations (e.g., Europe) and other regions with no stations (e.g., East Africa and most of Russia). Note also that the BSRN includes four stations on Antarctica.

## SURFRAD and SOLRAD

The SURFRAD and SOLRAD are two monitoring networks in the United States operated by the National Oceanic and Atmospheric Administration (NOAA). 

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
     height: 105px; 
     border:2px solid grey; 
     z-index: 9999;
     font-size:14px;">
     &nbsp;<b>Station network:</b><br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:blue"></i>&nbsp;SURFRAD<br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:red"></i>&nbsp;SOLRAD<br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:orange"></i>&nbsp;SRML<br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:green"></i>&nbsp;NREL<br>
</div>"""

m.get_root().html.add_child(folium.Element(legend_html))  # Add Legend

m.add_child(folium.LatLngPopup())  # Show latitude,longitude when clicking
m  # Show map

## University of Oregon - Solar Radiation Monitoring Laboratory (SRML)

The Solar Radiation Monitoring Laboratory (SRML) operates a network of station in the Northwestern United States. 

The following code cell will show how pvlib-python can be used to retrieve measured solar radiation data form the SRML network. The specific example extracts data from the Hermiston station for the month of June 2020. The *read_srml_month_from_solardat* function extracts data from the SRML archive, which stores data in monthly files for each station. A list of the station abbreviation can be found [here](http://solardat.uoregon.edu/StationIDCodes.html).

import pvlib
df = pvlib.iotools.read_srml_month_from_solardat(station='HE', year=2020, month=6)
df.head()

The output above shows the first five rows of the extracted data. We can now plot the parameters of interest, e.g., the three components of solar radiation; GHI, DNI, and DHI.

axes = df[['ghi_0', 'dni_0', 'dhi_3']].plot(subplots=True, figsize=(12,8), sharex=True, rot=0, legend=False)
axes[0].set_ylabel('GHI [W/m$^2$]')
axes[1].set_ylabel('DNI [W/m$^2$]')
axes[2].set_ylabel('DHI [W/m$^2$]')

## Future updates
Future updates to the this document will include the stations from the NREL and SRML networks.