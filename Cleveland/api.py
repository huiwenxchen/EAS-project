import csv
import json
import requests

def save_openaccess_results_to_file(department, skip=0, limit=5000, output_file='results.csv'):
    url = "https://openaccess-api.clevelandart.org/api/artworks"
    params = {
            'department': department,
            'skip': skip,
            'limit': limit,
            'has_image': 1
        }

    r = requests.get(url, params=params)

    data = r.json()

    headers = ['Title', 'Artist', 'Creation_Date', 'Accession_Number', 'Art_Type', 'Culture', 'Image']
    rows = []
    for artwork in data['data']:
        title = artwork['title']
        artist = artwork['creators'][0]['description'] if artwork['creators'] else "Unknown"
        creation_date = artwork['creation_date']
        accession_num = artwork['accession_number']
        art_type = artwork['type']
        culture = artwork['culture'][0] if artwork['culture'] else "Unknown"
        image = artwork['images']['web']['url']
        row = [title, artist, creation_date, accession_num, art_type, culture, image]
        rows.append(row)

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"{len(rows)} rows written to {output_file}")
    
if __name__ == '__main__':
    save_openaccess_results_to_file("Chinese Art", 0, 5000, 'art_results.csv')
