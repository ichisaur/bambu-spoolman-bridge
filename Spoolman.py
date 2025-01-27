import xml.etree.ElementTree as ET
from xmlrpc.client import DateTime
import requests
import datetime

class Vendor:
    id = ''
    registered = ''
    name = ''
    empty_spool_weight = ''
    extra = ''

    def __init__(self, id = '', registered = '', name = '', empty_spool_weight = '', extra = '' ):
        self.id = int(id)
        self.registered = registered
        self.name = name
        self.empty_spool_weight = float(empty_spool_weight)
        self.extra = extra
        
    def from_json(self, json):
        self.id = int(json['id'])
        self.registered = json['registered']
        self.name = json['name']
        self.empty_spool_weight = float(json['empty_spool_weight'])
        self.extra = json['extra']

class Filament:
    id = ''
    registered = ''
    name = ''
    vendor = Vendor()
    material = ''
    price = ''
    density = ''
    diameter = ''
    weight = ''
    spool_weight = ''
    color_hex = ''
    extra = ''
    idx = ''

    def __init__(self, 
             id = '',
             registered_t = '',
             name = '',
             vendor = '',
             material = '', 
             price = '',
             density = '',
             weight = '',
             spool_weight = '',
             color_hex = '', 
             extra = ''):
        
        self.id = int(id)
        self.registered = registered_t
        self.name = name
        self.vendor = vendor 
        self.material = material
        self.price = price
        self.density = density
        self.weight = weight
        self.spool_weight = spool_weight
        self.color_hex = color_hex
        self.extra = extra
        if extra:
            try:
                 self.idx = extra['idx']
            except:
                self.idx = ""


        
    def from_json(self, json):
        self.id = int(json['id'])
        self.registered = json['registered']
        self.name = json['name']
        self.vendor = Vendor().from_json(json['vendor'])
        self.material = json['material']
        self.price = json['price']
        self.density = json['density']
        self.weight = json['weight']
        self.spool_weight = json['spool_weight']
        self.color_hex = json['color_hex']
        self.extra = json['extra']
        if self.extra:
            try:
                 self.idx = self.extra['idx']
            except:
                self.idx = ""



class Spool:
    id = ""
    registered_t = ""
    first_used_t = ""
    last_used_t = ""
    filament = Filament()
    price = ""
    remaining_weight = ""
    initial_weight = ""
    spool_weight = ''
    used_weight = ''
    remaining_length = ''
    used_length = ''
    archived = False
    extra = ''

    def __init__(self, 
                 id = '',
                 registered_t = '',
                 first_used_t = '',
                 last_used_t = '',
                 filament = '', 
                 price = '',
                 remaining_weight = '', 
                 initial_weight = '',
                 spool_weight = '',
                 used_weight = '',
                 remaining_length = '',
                 used_length = '',
                 archived = '', 
                 extra = ''):
        
        self.id = int(id)
        self.registered_t = registered_t
        self.first_used_t = first_used_t
        self.last_used_t = last_used_t
        self.filament = filament
        self.price = price
        self.remaining_weight = remaining_weight
        self.initial_weight = initial_weight
        self.spool_weight = spool_weight
        self.used_weight = used_weight
        self.remaining_length = remaining_length
        self.used_length = used_length
        self.archived = archived
        self.extra = extra


    def from_json(self, json):
        self.id = int(json['id'])
        self.registered_t = json['registered']
        self.first_used_t = json['first_used']
        self.last_used_t = json['last_used']
        self.filament = Filament().from_json(json['filament'])
        self.price = json['price']
        self.remaining_weight = json['remaining_weight']
        self.initial_weight = json['initial_weight']
        self.spool_weight = json['spool_weight']
        self.used_weight = json['used_weight']
        self.remaining_length = json['remaining_length']
        self.used_length = json['used_length']
        self.archived = json['archived']
        self.extra = json['extra']

    


class SpoolmanHandler:
    
    api_url = ""

    def __init__(self, ipaddress, port = 7912):
        self.api_url = f"{ipaddress}/api/v1/"

    def find_filament(self, material, idx, color_hex, threshold = 20):
        query = 'filament'
        payload = { 
            'material' : material,
            'idx' : idx,
            'color_hex' : color_hex,
            'color_similarity_threshold' : threshold
        }
        query_url = f"{self.api_url}{query}"
        response = requests.get(query_url, params = payload)

        if response.status_code() == 200: 
            filament = Filament()
            filament.from_json(response.json()[0])
            return filament
        else:
            raise ConnectionError(f"Error. Response Code {response.status_code()}.")
        
       
#    def find_filament_id(self, material, idx, color_hex, threshold = 20):
#        return self.find_filament(material  =   material,
#                                  idx       =   idx,
#                                  color_hex =   color_hex,
#                                  threshold =   threshold)[0]['id']

        
    def find_spool(self, filament):
        
        query = 'spool'
        query_url = f"{self.api_url}{query}"
        payload = {
            'filament.id' : filament.id,
            'sort' : 'spool_weight:asc'
        }

        response = requests.get(query_url, params = payload)

        if response.status_code() == 200: 
            spool = spool()
            spool.from_json(response.json()[0])
            return spool
        else:
            raise ConnectionError(f"Error. Response Code {response.status_code()}.")
                
                
            



    def use_filament_by_weight(self, filament, weight):
        spool = self.find_spool(filament)
        
        return self.use_weight(spool, weight=weight)
    
    def use_weight(self, spool, weight):
        query = f'spool/{spool.id}/use'
        payload = {
            'use_weight' : weight
        }
        query_url = f"{self.api_url}{query}"
        response = requests.put(query_url, json = payload)

        return response

