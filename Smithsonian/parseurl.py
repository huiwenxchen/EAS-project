import json
import requests
import csv
import urllib.request
import os

# Make the request and get the text content of the response

def create_csv():
    headers = ['Title','Artist','Creation_Date','Accession_Number','Art_Type','Culture','Image']
    with open('smithsonian_chinese.csv', 'w', newline='') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(headers)

def parse_txt(url):
    link = 'https://asia.si.edu/explore-art-culture/collections/search/'
    response = requests.get(url)
    filename = os.path.basename(url)
    filename_part = filename.split('.')[0][-2:]

    # file cannot be directly converted to json
    # with open(f'{filename_part}.txt', 'w') as file:
    #     file.write(response.text)
    #     file.flush()

    with open(f'{filename_part}.txt', 'r') as file:
        lines = file.readlines()

    lines = [line.strip() + ',' for line in lines]

    # Convert each line to JSON object
    json_list = []
   # headers = ['Title','Artist','Creation_Date','Accession_Number','Art_Type','Culture','Image']
    with open('smithsonian_chinese.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # writer.writerow(headers)
        for line in lines:
            json_content = json.loads(line[:-1])
            culture = json_content['content']['indexedStructured']['culture'] if "culture" in json_content['content']['indexedStructured'] else []
            place = json_content['content']['indexedStructured']['place'][0] if "place" in json_content['content']['indexedStructured'] else []
            if "Chinese" in culture or "China" in place:
                freetext = json_content['content']['freetext']
                Title = json_content['title']
                Image = json_content['content']['descriptiveNonRepeating']['online_media']['media'][0]['content']
                #art_url = link + json_content['url']
                Creation_Date = freetext['date'][0]['content']
                #dynasty = freetext['date'][1]['content']
                Accession_Number = freetext['identifier'][0]['content']
                Artist = freetext['name'][0]['content'] if "name" in freetext else ""
                #medium = freetext['physicalDescription'][0]['content']
                Art_Type = freetext['objectType'][0]['content']
                Culture = "Chinese"
                json_list.append({"Title":Title, "Artist":Artist, "Creation_Date": Creation_Date, "Accession_Number":Accession_Number, "Art_Type":Art_Type, "Culture":"China", "Image":Image})
                writer.writerow([Title, Artist, Creation_Date, Accession_Number, Art_Type, Culture, Image])

# open the base url and read through each line. for each line, call parse_text() passing the line as the url


index_url = "https://smithsonian-open-access.s3-us-west-2.amazonaws.com/metadata/edan/fsg/index.txt"

with urllib.request.urlopen(index_url) as f:
    create_csv()
    for i in f:
        print(i.decode("utf-8").strip())
        parse_txt(i.decode("utf-8").strip())