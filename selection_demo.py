from PIL import Image
import numpy as np
import xml.etree.ElementTree as ET

pick_path = 'temp/pick_6.png' #Path to pick png
slice_config_path = 'temp/Metadata/slice_info.config' #Path to slice config file

im = Image.open(pick_path) 
im = im.convert('RGBA')

green_pick_data = np.array(im)

red, green, blue, alpha = green_pick_data.T

red_areas = (blue == 0) & (alpha == 255)
green_pick_data[..., :-1][red_areas.T] = (0, 255, 0)

green_pick_im = Image.fromarray(green_pick_data)
green_pick_im.show()

slice_XML = ET.parse(slice_config_path)
object_info = []
for object in slice_XML.iter('object'):
    object_info.append(object.attrib)

print("List of Objects:")
for object in object_info:
    
    print(f"ID: {"{:<10}".format(object['identify_id'])} Name: {object['name']}")


obj_list = []
confirm = 0
while 1:

    input_str = input("Enter ID of object you wish you select/deselect, 'Confirm' to confirm: ")

    if input_str == 'Confirm' :
        print('Cancelling following Objects IDs: ')
        for obj in obj_list:
            print(obj)

        cancel_pick_data = confirm_pick_data
        red, green, blue, alpha = cancel_pick_data.T
        cancel_areas = (red == 255) & (green ==  255) 
        cancel_pick_data[..., :-1][cancel_areas.T] = (255, 0, 0)
        Image.fromarray(cancel_pick_data).show()

    else:
        if int(input_str) in obj_list:
            obj_list = list(filter(lambda a: a != int(input_str), obj_list))
        else: 
            obj_list.append(int(input_str))
        print(obj_list)
        confirm_pick_data =  np.array(im)
        red, green, blue, alpha = confirm_pick_data.T
        for obj in obj_list: 
            red_channel = obj % 256
            green_channel = obj // 256
            confirm_areas = (red == red_channel) & (green == green_channel) & (blue == 0) & (alpha == 255)
            confirm_pick_data[..., : -1][confirm_areas.T] = (255, 255, 0)

        confirm_areas = (red != 255) & (green != 255) & (blue == 0) & (alpha == 255)
        confirm_pick_data[..., : -1][confirm_areas.T] = (0, 255, 0)
        Image.fromarray(confirm_pick_data).show()









