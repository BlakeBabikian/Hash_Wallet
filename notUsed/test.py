import geoip2.database

# Open the GeoIP2 database
reader = geoip2.database.Reader('path/to/GeoLite2-City.mmdb')

# Look up information about an IP address
response = reader.city('8.8.8.8')

# Extract information from the response
print('Country:', response.country.name)
print('Region:', response.subdivisions.most_specific.name)
print('City:', response.city.name)
print('Postal Code:', response.postal.code)
print('Latitude:', response.location.latitude)
print('Longitude:', response.location.longitude)
print('Time Zone:', response.location.time_zone)

# Close the database
reader.close()
