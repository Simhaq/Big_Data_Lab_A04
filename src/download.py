import os
import random
import yaml
import pandas as pd

from bs4 import BeautifulSoup

# Getting the parameters ( year and n_locs from params.yaml 
with open('params.yaml') as f:
    params = yaml.safe_load(f)

cwd = os.getcwd()
year = params['download']['year']

url = f'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}'  # The url where the data archive is present

# Funtion to extract csv file urls to be downloaded and store it in url_list.txt 
def extract_files():
    with open(year,'r') as f:
        page = f.read()
    f.close()
    soup = BeautifulSoup(page, 'html.parser')                      # Parse the html file and extract the csv files
    files = [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith('csv')]
    
    n_files = params['download']['n_locs'] 
    n_files = min(n_files,len(files))
    random.shuffle(files)                                          # Randomizing for multiple runs

    print("Selecting Files containing monthly averages...")
    count = 0
    txt = open('url_list.txt','w')

    
    for f in files:
        csv = pd.read_csv(f)
        if csv['MonthlyStationPressure'].count() == 12:           # Checking whether monthly averages are present for 12 
            count +=1                                             # months before downloading (Handling NULL values)
            print(f"{count}/{n_files} files selected")
            txt.write(f+'\n')                                     # Writing the url of csv file for downloading
            
        if count == n_files:
            break
            
    txt.close()

# wget to download the page containing csv files for an year
os.system(f"wget {url} -P {cwd}")

extract_files()

# Downloading the csv files and placing it in the data folder
os.system(f"wget --input-file {cwd}/url_list.txt -P {cwd}/data/climate_data")

# Removing unwanted files
os.remove(f'{cwd}/{year}')
os.remove(os.path.join(cwd,"url_list.txt"))