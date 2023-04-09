import os
import xml.etree.ElementTree as ET

def convert_voc_to_yolo(xml_file_path,txt_file_path):
    print("xml_file_path:",xml_file_path)
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    image_width = int(root.find('size').find('width').text)
    image_height = int(root.find('size').find('height').text)


    yolo_labels = []
    for obj in root.findall('object'):
        
        name = obj.find('name').text
        bndbox = obj.find('bndbox')
        x_min = int(bndbox.find('xmin').text)
        y_min = int(bndbox.find('ymin').text)
        x_max = int(bndbox.find('xmax').text)
        y_max = int(bndbox.find('ymax').text)
        w = x_max - x_min
        h = y_max - y_min

        x_center = x_min + w / 2
        y_center = y_min + h / 2

        x_center /= image_width
        y_center /= image_height
        w /= image_width
        h /= image_height
        if name=="car":name=0
        elif name=="barrier" or name=="barrierw":name=1
        elif name=="green":name=2
        elif name=="red":name=3
        yolo_labels.append(f'{name} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}')

    with open(txt_file_path, 'w') as f:
        f.write('\n'.join(yolo_labels))

# Example usage


directory = '/training_traffic/labels'

for filename in os.listdir(directory):
    if filename.endswith('.xml'):
        print("file:",filename)
        # do something with root

        xml_file_path = filename
        txt_file_path = filename.replace("xml","txt")

        yolo_labels = convert_voc_to_yolo("labels/"+xml_file_path,"labels_n/"+txt_file_path)
        print(yolo_labels)



#import os
# import glob
# import xml.etree.ElementTree as ET

# def xml_to_txt(path):
#     print("path:",path)
#     for xml_file in glob.glob(path + '/*.xml'):
#         print("path + '/*.xml':",path + '/*.xml')

#         tree = ET.parse(xml_file)
#         root = tree.getroot()
#         txt_file_path = xml_file.replace('.xml', '.txt')
#         with open(txt_file_path, 'w') as txt_file:
#             for member in root.findall('object'):
#                 bbox = member.find('bndbox')
#                 class_name = member.find('name').text
#                 if class_name=="car":class_name=0
#                 elif class_name=="barrier":class_name=1
#                 elif class_name=="green":class_name=2
#                 elif class_name=="red":class_name=3
#                 x_min, y_min, x_max, y_max = bbox.find('xmin').text, bbox.find('ymin').text, bbox.find('xmax').text, bbox.find('ymax').text
#                 txt_file.write(f'{class_name} {x_min} {y_min} {x_max} {y_max}\n')
# xml_to_txt("labels")