
from PIL import Image
import numpy as np
import xml.etree.ElementTree as ET

class pickPNG:

    def __init__(self, path_to_png):
        self.im = Image.open(path_to_png).convert('RGBA')
        self.im_data = np.array(self.im)


    def _color_swapper(self, image_data, color_from, color_to): 
        working_data = image_data
        
        
        red, green, blue, alpha = working_data.T
        
        pick_areas = (red == color_from[0]) & (green == color_from[1]) & (blue == color_from[2]) & (alpha == color_from[3])
        
        working_data[..., :-1][pick_areas.T] = (color_to[0], color_to[1], color_to[2])
        return working_data
    
    def _color_from_id(self, ID): 
        r = ID % 256
        g = ID // 256
        b = 0
        a = 255
        return (r, g, b, a)

    def generate_pick_image(self, select_list = [], canceled_list = []): 
        data = np.array(self.im)

        for id in select_list:
            target_color = self._color_from_id(id)
            print(target_color)
            data = self._color_swapper(data, target_color, (255, 255, 1, 255))
        
        for id in canceled_list:
            target_color = self._color_from_id(id)
            data = self._color_swapper(data, target_color, (255, 0, 1, 255))

        red, green, blue, alpha = data.T
        
        pick_areas = (blue == 0) & (alpha == 255)
        
        data[..., :-1][pick_areas.T] = (0, 255, 0)

        return Image.fromarray(data)



    



pick_path = 'temp/pick_6.png' #Path to pick png
slice_config_path = 'temp/Metadata/slice_info.config' #Path to slice config file

im = pickPNG(pick_path)



slice_XML = ET.parse(slice_config_path)
object_info = []
for object in slice_XML.iter('object'):
    object_info.append(object.attrib)

im.generate_pick_image().show()

print("List of Objects:")
for object in object_info:
    
    print(f"ID: {"{:<10}".format(object['identify_id'])} Name: {object['name']}")


obj_list = []
canceled_list = []
confirm = 0
while 1:

    input_str = input("Enter ID of object you wish you select/deselect, 'Confirm' to confirm: ")

    if input_str == 'Confirm' :
        print('Cancelling following Objects IDs: ')
        for obj in obj_list:
            print(obj)
        canceled_list = obj_list
        obj_list = []
        im.generate_pick_image(select_list=obj_list, canceled_list=canceled_list).show()


    else:
        if int(input_str) in obj_list:
            obj_list = list(filter(lambda a: a != int(input_str), obj_list))
        else: 
            obj_list.append(int(input_str))

        im.generate_pick_image(select_list=obj_list, canceled_list=canceled_list).show()









