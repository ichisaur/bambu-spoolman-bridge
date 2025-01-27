import zipfile
import xml.etree.ElementTree as ET
import requests
import yaml
from bambuFTP import BambuPrinterFTP
import os
import Spoolman


class Parse3MF:
    path = ""
    slice_config = ""

    def __init__(self, path):
        self.path = path


class SpoolmanHandler:

    def __init__(self, ipaddress):

        return
    
    
with open('secrets.yml', 'r') as file:
    secrets = yaml.safe_load(file)
print(secrets)

device_ip = secrets['device_ip']
access_code = str(secrets['access_code'])
spoolman_url = secrets['spoolman_ip']

bambu = BambuPrinterFTP(device_ip=device_ip, access_code= access_code)


tempdir = "./temp/"

if __debug__:
    pass
else:
    bambu.connect()
    bambu.get_file('AAA-Cover_Plate_3.gcode.3mf')
    bambu.close_connection()


with zipfile.ZipFile('./temp/temp.3mf') as zip_ref:
    zip_ref.extract('Metadata/slice_info.config', 'temp/')

slice_XML = ET.parse('temp/Metadata/slice_info.config')
filament_info = []
for filament in slice_XML.iter('filament'):
    filament_info.append(filament.attrib)

#print(filament_info)

plate_index = -1
for metadata in slice_XML.iter('metadata'):
    if metadata.attrib['key'] == "index":
        plate_index = metadata.attrib["value"]
        break

# print(plate_index)

with zipfile.ZipFile('./temp/temp.3mf') as zip_ref:
    path = zip_ref.extract(f'Metadata/plate_{plate_index}.png', 'temp/')
    os.replace(path, 'temp/preview.png')

spoolman_service = Spoolman.SpoolmanHandler(spoolman_url)

for filament in filament_info:
    type = filament['type']
    idx = filament['tray_info_idx']
    color = filament['color'][1:]

    sm_filament = spoolman_service.find_filament(material= type, idx= idx, color_hex= color)
    
    if sm_filament.id != "":

        result = spoolman_service.use_filament_by_weight(sm_filament, filament['used_g'])
        print(result)




#ftp.connect(host = device_ip, port = 990, timeout = 20)
##print('Logging In') 
#ftp.login(user = user, passwd = access_code)
#ftp.prot_p()
#print('Sucess')
#
#with open('temp.3mf', 'wb') as fp:
#    ftp.retrbinary('RETR Spools_Plate_6.gcode.3mf', fp.write)
#
#ftp.quit()

