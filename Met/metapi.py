import requests
import json
import csv


url = "https://www.metmuseum.org/api/collection/collectionlisting"
base_url = "https://images.metmuseum.org/CRDImages/"
params = {
    'geolocation': 'China',
    'showOnly': 'openAccess',
    'department': 6,
    'offset': 0
}

increment = 40
max_offset = 11440
headers = ['Title','Artist','Creation_Date','Accession_Number','Art_Type','Culture','Image']
results = []

while params['offset'] <= max_offset:
    response = requests.get(url, params=params)
    json_data = json.loads(response.text)
    results += json_data['results']
    print(params['offset'])
    params['offset'] += increment


with open('met.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(headers)
    

    for result in results:
        # if there is time, make a single function for the ... if...else 
        Title = result.get('title', '') if result.get('title', '') else "Unknown title"
        Artist = result.get('artist', '') if result.get('artist', '') else "Unidentified Artist"
        Culture = result.get('culture', '') if result.get('culture', '') else "Unknown Culture"
        Accession_Number = result.get('accessionNumber', '') if result.get('accessionNumber', '') else "Unknown Accession Number"
        Creation_Date = result.get('date', '') if result.get('date', '') else "Unknown Date"
        Art_Type = result.get('medium', '') if result.get('medium', '') else "Unknown Medium or Art Type"
        Image = result.get('image', '') if result.get('image', '') else base_url + result.get('regularImage', '') 
        
        writer.writerow([Title, Artist, Creation_Date, Accession_Number, Art_Type, Culture, Image])


