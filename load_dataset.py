import os
import requests
import json
from bs4 import BeautifulSoup


def process_yml_files(path):

    plume_path = os.path.join("dataset", path) # path = plume(nasa)
    
    if not os.path.exists(plume_path):
        raise FileNotFoundError(f"Directory not found: {plume_path}")
    
    result = []
    
    for recorder in os.listdir(plume_path):
        yml_files = os.path.join(plume_path, recorder)
        if not os.path.isdir(yml_files):
            continue

        for root, _, files in os.walk(yml_files): # for subdir containg .yml inside yml_files
            ymls = [f for f in files if f.endswith('.yml')]

            for yml in ymls:
                
                yml_path = os.path.join(yml_files,yml)
                img_path = yml_path.removesuffix(".yml") + ".jpg"
                result.append({
                     "parent_path": yml_files,
                     "yml_path": yml_path,
                     "img_path": img_path,
                     "label_info":yml 
                })
       
    return result


def save_images(label_info: str, img_path: str):
    # example label_info input: lor_0034583522_0x630_sci.yml
    if label_info.endswith(".yml"): # all
        label_info = label_info.removesuffix(".yml")

    if label_info.startswith("E"): # messangers 
         label_info = label_info.removeprefix("E")

    if label_info.endswith("_1__label"): # cassini
         label_info = label_info.removesuffix("_1__label")

    if label_info.endswith("_label"): # all
         label_info = label_info.removesuffix("_label")
    


    url = requests.get(f"https://pds-imaging.jpl.nasa.gov/solr/pds_archives/search?identifier=*{label_info}*")

    url_load = BeautifulSoup(url.text,'html.parser')

    url_load_json = json.loads(url_load.text)

    image_s = url_load_json['response']['docs'][0]['ATLAS_BROWSE_URL']



    response = requests.get(image_s)
    if response.status_code == 200:
        with open(img_path, "wb") as file:
                file.write(response.content)
    else:
        print(f"got {response.status_code} for {img_path}")
    return response
