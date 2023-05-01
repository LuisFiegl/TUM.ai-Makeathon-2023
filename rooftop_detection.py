# %%
# Looking at the OSM Building Data
import osmium

class NodeHandler(osmium.SimpleHandler):
    def node(self, n):
        print(n)

handler = NodeHandler()
handler.apply_file("./bremen-buildings-only.osm.pbf")
# %%
# Define a handler for buildings
class BuildingHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.buildings = []
        self.building_apex_height = []
        self.roof_apex = []
        self.height = []

    def node(self, n):
        if 'building' in n.tags and n.tags['building'] == 'yes':
            self.buildings.append((n.location.lat, n.location.lon))
        if 'building:apex:height' in n.tags and n.tags['building:apex:height'] == 1:
            self.building_apex_height.append((n.location.lat, n.location.lon))
        if 'roof:apex' in n.tags and n.tags['roof:apex'] == "yes":
            self.roof_apex.append((n.location.lat, n.location.lon))
        if 'height' in n.tags:
            self.roof_apex.append((n.location.lat, n.location.lon))

    def way(self, w):
        if 'building' in w.tags and w.tags['building'] == 'yes':
            buildings_nodes = [(n.location.lat, n.location.lon) for n in w.nodes if n.location == True]
            if buildings_nodes:
                self.buildings.extend(buildings_nodes)

# Read the .osm.pbf file and extract building locations
file_name = "./bremen-buildings-only.osm.pbf"
handler = BuildingHandler()
handler.apply_file(file_name)
# %%
# Creating a dataframe with coordinate data
import pandas as pd
df = pd.DataFrame(handler.roof_apex, columns=['latitude', 'longitude'])
df
# %%
# Also showing the tags
class BuildingHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.buildings = []

    def node(self, n):
        self.buildings.append((n.location.lat, n.location.lon, list(n.tags)))

# Read the .osm.pbf file and extract building locations
file_name = "./bremen-buildings-only.osm.pbf"
handler = BuildingHandler()
handler.apply_file(file_name)

df_all = pd.DataFrame(handler.buildings, columns=['latitude', 'longitude', "tags"])
df_all

# %%
# The same for whole Germany
class BuildingHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.buildings = []
        self.building_apex_height = []
        self.roof_apex = []
        self.height = []

    def node(self, n):
        if 'building' in n.tags:
            self.buildings.append((n.location.lat, n.location.lon, n.tags['building']))
        if 'building:apex:height' in n.tags:
            self.building_apex_height.append((n.location.lat, n.location.lon, n.tags['building:apex:height']))
        if 'roof:apex' in n.tags:
            self.roof_apex.append((n.location.lat, n.location.lon, n.tags['roof:apex']))
        if 'height' in n.tags:
            self.height.append((n.location.lat, n.location.lon, n.tags['height']))

    def way(self, w):
        if 'building' in w.tags and w.tags['building'] == 'yes':
            buildings_nodes = [(n.location.lat, n.location.lon) for n in w.nodes if n.location == True]
            if buildings_nodes:
                self.buildings.extend(buildings_nodes)

# Read the .osm.pbf file and extract building locations
file_name = "./germany-buildings-only.osm.pbf"
handler = BuildingHandler()
handler.apply_file(file_name)

import pandas as pd
df = pd.DataFrame(handler.buildings, columns=['latitude', 'longitude', "extra"])
df
# %%
# Looking at the map
import folium

# Create a map centered on Bremen
map = folium.Map(location=[53.0793, 8.8017], zoom_start=12)

# Add markers for each coordinate in the DataFrame
for index, row in df_all[df_all["tags"].str.len() != 0][0:1000].iterrows():
    folium.Marker(location=[row['latitude'], row['longitude']]).add_to(map)

# Display the map
map

# %%
#Using a pre-trained model for visual roof detection

import torch
from unet import *
%load_ext autoreload
%autoreload 2
# Load the model
device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
map_location=torch.device('cpu')
path = './batch5_loss4_1000.pt'
model = UNet(3,1,False).to(device)
model.load_state_dict(torch.load(path, map_location=map_location))

# %%
#Applying the model on a picture from Google Satellite
from import_test import *
import_and_show(model,'test5.PNG')
# %%
