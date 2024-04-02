import os
import yaml
from bs4 import BeautifulSoup

from zipfile import ZipFile 

import random


with open('params.yaml') as f:
    params = yaml.safe_load(f)

cwd = os.getcwd()
year = params['download']['year']

url = f'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}'

def extract_files():
    with open(year,'r') as f:
        page = f.read()
    f.close()
    soup = BeautifulSoup(page, 'html.parser')
    files = [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith('csv')]
    
    n_files = params['download']['n_locs'] 
    n_files = min(n_files,len(files))
    files = random.sample(files, n_files)
    
    with open('url_list.txt','w') as f:
        for file in files:
            f.write(file+'\n')
    f.close()


os.system(f"wget {url} -P {cwd}")

extract_files()

os.system(f"wget --input-file {cwd}/url_list.txt -P {cwd}/data")

os.remove(f'{cwd}/{year}')
os.remove(os.path.join(cwd,"url_list.txt"))