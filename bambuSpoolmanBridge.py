import appdaemon.plugins.hass.hassapi as hass
import bambuFTP
import xml.etree.ElementTree as ET
from bambuFTP import BambuPrinterFTP
import os
import Spoolman
import zipfile


class bambuSpoolman(hass.Hass):


    def initialize(self): 
        self.log("Initializing Bambu Spoolman Bridge.")
        self.listen_state(self.getInfo, self.args['print_status_sensor'], new = "running")
        
        
    def getInfo(self, entity, attribute, old, new, kwargs):
        self.log("New Print Detected.")

        device_ip = self.args['device_ip']
        access_code = str(self.args['access_code'])
        spoolman_url = self.args['spoolman_ip']

        bambu = BambuPrinterFTP(device_ip=device_ip, access_code= access_code)


        tempdir = "./temp/"


        bambu.connect()
        gcode_name = self.get_state(self.args['gcode_sensor'])
        self.log(f"Obtaining GCode File: {gcode_name}")
        bambu.get_file(gcode_name)
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
                #print(result)





    
