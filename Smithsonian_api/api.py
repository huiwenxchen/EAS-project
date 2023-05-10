import requests
import json
import csv


url = "https://api.si.edu/openaccess/api/v1.0/search"
params = {
    'q':'culture=Chinese',
    'api_key':'TQtiHgdkwaNXOmahQycjgZDWK45AFmYUJRZtL9wH'
}


headers = ['Title','Artist','Creation_Date','Accession_Number','Art_Type','Culture','Image']
results = []

response = requests.get(url, params=params)
json_data = json.loads(response.text)
results = json_data['response']['rows']

with open("api_query.json", "w") as f:
    json.dump(results, f)

print('Results saved as results.json')
