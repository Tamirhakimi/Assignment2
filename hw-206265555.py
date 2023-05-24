# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:03:28 2023

@author: tamir
"""

import requests
import pandas as pd

# Read destinations from file
with open('dests.txt', 'r') as file:
    destinations = [line.strip() for line in file.readlines()]

# Initialize empty dataframe
df = pd.DataFrame(columns=['Target', 'Distance_km', 'Duration', 'Longitude', 'Latitude'])

# Google Maps API endpoints
distance_matrix_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
geocoding_url = 'https://maps.googleapis.com/maps/api/geocode/json'

# API parameters and credentials
params = {
    'origins': 'Tel Aviv',
    'units': 'metric',
    'key': 'YOUR_DISTANCE_MATRIX_API_KEY'
}

geocode_params = {
    'key': 'YOUR_GEOCODING_API_KEY'
}

# Iterate over destinations
for destination in destinations:
    params['destinations'] = destination
    geocode_params['address'] = destination
    
    # Get distance and duration from Distance Matrix API
    response = requests.get(distance_matrix_url, params=params)
    distance_data = response.json()
    
    # Get longitude and latitude from Geocoding API
    geocode_response = requests.get(geocoding_url, params=geocode_params)
    geocode_data = geocode_response.json()
    
    # Extract required information from API responses
    distance_km = distance_data['rows'][0]['elements'][0]['distance']['text']
    duration = distance_data['rows'][0]['elements'][0]['duration']['text']
    longitude = geocode_data['results'][0]['geometry']['location']['lng']
    latitude = geocode_data['results'][0]['geometry']['location']['lat']
    
    # Append data to the dataframe
    df = df.append({
        'Target': destination,
        'Distance_km': distance_km,
        'Duration': duration,
        'Longitude': longitude,
        'Latitude': latitude
    }, ignore_index=True)

# Print dataframe contents
print(df)

# Find the three cities furthest from Tel Aviv
furthest_cities = df.nlargest(3, 'Distance_km')
print(furthest_cities)