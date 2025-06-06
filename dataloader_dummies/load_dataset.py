import os
import requests
import json
import yaml
from bs4 import BeautifulSoup
from pprint import pprint

galileo_images = {
    # Callisto images
    "2900r_label.yml": "G2C0004",
    "6200r_label.yml": "G7C0001",
    "1600r_label.yml": "30C0027",
    "1901r_label.yml": "30C0028",
    "2201r_label.yml": "30C0029",
    "4300r_label.yml": "31C0001",
    "4301r_label.yml": "31C0001",
    
    # Europa images
    "5139r_label.yml": "G1E0004",
    "4500r_label.yml": "G7E0010",
    "2778r_label.yml": "10E0001",
    "4626r_label.yml": "12E0003",
    "4639r_label.yml": "12E0004",
    "4652r_label.yml": "12E0005",
    "4842r_label.yml": "14E0054",
    "4878r_label.yml": "14E0056",
    "4901r_label.yml": "14E0057",
    "4914r_label.yml": "14E0058",
    "4965r_label.yml": "14E0062",
    "4978r_label.yml": "14E0063",
    "5000r_label.yml": "14E0064",
    "5026r_label.yml": "14E0066",
    "5039r_label.yml": "14E0067",
    "5052r_label.yml": "14E0068",
    "4429r_label.yml": "15E0096",
    "4726r_label.yml": "19E0008",
    "6314r_label.yml": "25E0021",
    "6366r_label.yml": "25E0025",
    "6427r_label.yml": "25E0029",
    "6452r_label.yml": "25E0031",
    
    # Ganymede images
    "1000r_label.yml": "C9G0010",
    "1013r_label.yml": "C9G0011",
    "1026r_label.yml": "C9G0012",
    "1039r_label.yml": "C9G0013",
    "1078r_label.yml": "C9G0016",
    "1500r_label.yml": "E6G0020",
    "1513r_label.yml": "E6G0021",
    "2000r_label.yml": "G1G0001",
    "3078r_label.yml": "14G0001",
    "6900r_label.yml": "20G0001",
    "7600r_label.yml": "30G0003",
    "7900r_label.yml": "30G0004",
    "8200r_label.yml": "30G0005",
    
    # Io images
    "1300r_label.yml": "C3I0040",
    "3178r_label.yml": "C9I0015",
    "3200r_label.yml": "C9I0016",
    "3204r_label.yml": "C9I0017",
    "3207r_label.yml": "C9I0018",
    "6300r_label.yml": "G2I0020",
    "8645r_label.yml": "G8I0010",
    "8700r_label.yml": "G8I0011",
    "8723r_label.yml": "G8I0012",
    "5045r_label.yml": "G8I0013",
    "5100r_label.yml": "G8I0014",
    "5123r_label.yml": "G8I0015",
    "2445r_label.yml": "G8I0019",
    "4204r_label.yml": "10I0028",
    "4207r_label.yml": "10I0029",
    "0085r_label.yml": "11I0012",
    "3485r_label.yml": "11I0015",
    "5146r_label.yml": "31I0001",
    "5147r_label.yml": "31I0001",
    "5546r_label.yml": "31I0003",
    "5547r_label.yml": "31I0003"
}


def process_yml_files(path):
    """
        loop all .yml files in through dataset/{path},
        
        
        return  [
            ...,
            {
                "parent_path": yml_files, // yaml file's parent directory Info.
                "yml_path": yml_path, // parent dir + yaml file path
                "img_path": img_path, // parent dir + image file path(same name as .yml file, but .yml -> .jpg)
                "label_info": yml 
            }
            ...,
            ...,
        ]
    """
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
    # galileo_specific
    if label_info in galileo_images.keys():
        return None
    #precondition & process
    if label_info.endswith(".yml"): # all
        label_info = label_info.removesuffix(".yml")

    if label_info.startswith("E"): # messangers 
        label_info = label_info.removeprefix("E")

    if label_info.endswith("_1_label"): # cassini
        label_info = label_info.removesuffix("_1_label")

    if label_info.endswith("_label"): # all
        label_info = label_info.removesuffix("_label")
    

    


    link = f"https://pds-imaging.jpl.nasa.gov/solr/pds_archives/search?identifier=*{label_info}*"
    url = requests.get(link)

    url_load = BeautifulSoup(url.text,'html.parser')

    url_load_json = json.loads(url_load.text)
    image_s = url_load_json['response']['docs'][0]['ATLAS_BROWSE_URL']
    


    response = requests.get(image_s)
    if response.status_code == 200:
        with open(img_path, "wb") as file:
                file.write(response.content)
    else:
        print(f"got {response.status_code} with {response} for {img_path} for {link}")
    return response








#galileo specific
def find_and_transform_url(label_info, label_info_2):
    search_url = f"https://pds-imaging.jpl.nasa.gov/search/?fq=-ATLAS_THUMBNAIL_URL%3Abrwsnotavail.jpg&q={label_info}"
    
    try:
        response = requests.get(search_url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        image_urls = []
        for tag in soup.find_all(['a', 'img', 'link']):  
            href = tag.get('href') or tag.get('src')
            if href and '/thumbnail/' in href and f'{label_info_2}.jpeg' in href:
                image_urls.append(href)
        
        if not image_urls or len(image_urls) > 1:
            print(f"No matching URLs found for label_info: {label_info} in {image_urls}")
            return None
        
        url = image_urls[0]
        
        url = url.replace('/thumbnail/', '/browse/')
        
        return url
        

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None




def only_plumes(path='plume(nasa)',destiny_folder='../dataset/filtered_plumes/'):
    plume_path = os.path.join("dataset", path)  # path = plume(nasa)
    
    if not os.path.exists(plume_path):
        plume_path = os.path.join("../dataset",path)
        if not os.path.exists(plume_path):
            raise FileNotFoundError(f"Directory not found: {plume_path}")
    
    index = 0 
    
    for recorder in os.listdir(plume_path):
        yml_files = os.path.join(plume_path, recorder)
        if not os.path.isdir(yml_files):
            continue

        for _, _, files in os.walk(yml_files):  
            ymls = [f for f in files if f.endswith('.yml')]

            for yml in ymls:
                yml_path = os.path.join(yml_files, yml)
                img_path = yml_path.removesuffix(".yml") + ".jpg" 

                if not os.path.exists(img_path):
                    continue 
                
                with open(yml_path, 'r') as yml_file:
                    yml_data = yaml.safe_load(yml_file)
                
                if 'plumes' in yml_data:
                    destination_yml = os.path.join(destiny_folder, f"{index}.yml")
                    destination_img = os.path.join(destiny_folder, f"{index}.jpg")
                    
                    #with open(destination_yml, 'w') as new_yml_file:
                        #yaml.dump(yml_data, new_yml_file)
                    
                    with open(img_path, 'rb') as img_file:
                        with open(destination_img, 'wb') as new_img_file:
                            new_img_file.write(img_file.read())
                    
                    index += 1  
                    
                    
    print(f"Processed {index} number of images in total.")
