from xml.dom import minidom
from os import path, replace, scandir, remove
import xml.etree.ElementTree as ET
import cv2


def notext(f):
    return path.splitext(f.name)[0]


raw_img = list(
    sorted(scandir('img_val'), key=lambda f: f.name)
)
raw_label = list(
    sorted(scandir('anno_val'), key=lambda f: f.name)
)

csv_files = [f for f in raw_label if f.name.endswith('xml')]
jpg_files = [f for f in raw_img if f.name.endswith('jpg')]

for i, (f_jpg, f_csv) in enumerate(zip(jpg_files, csv_files)):
    if notext(f_jpg) != notext(f_csv):
        raise ValueError('Raw data filenames mismatch')

    img = cv2.imread(f_jpg.path)
    xml_content = minidom.parse(f_csv.path)
    xmins = xml_content.getElementsByTagName('xmin')
    ymins = xml_content.getElementsByTagName('ymin')
    xmaxs = xml_content.getElementsByTagName('xmax')
    ymaxs = xml_content.getElementsByTagName('ymax')
    name = str(xml_content.getElementsByTagName('filename')[0].firstChild.data)
    print(name)
    for i in range(2):
        xmin = int(xmins[i].childNodes[0].data)
        ymin = int(ymins[i].childNodes[0].data)
        xmax = int(xmaxs[i].childNodes[0].data)
        ymax = int(ymaxs[i].childNodes[0].data)
        croped = img[ymin:ymax, xmin:xmax]

        if i == 0:
            electricity_meter = 'counter_val/'+str(i)+name
            cv2.imwrite(electricity_meter, croped)
        # elif i == 0:
        #     electricity_meter = 'electricity_meter/'+str(i)+name
        #     cv2.imwrite(electricity_meter, croped)


# <annotation>
# <folder>img_labeled</folder>
# <filename>20201015_153316_resize.jpg</filename>
# <path>C:\Users\Khoi Tran\Desktop\hk1-Năm 3\Các vấn đề NC&UD trong CS\dataset_for_object_detection\img_labeled\20201015_153316_resize.jpg</path>
# <source>
#   <database>Unknown</database>
# </source>
# <size>
#   <width>604</width>
#   <height>806</height>
#   <depth>3</depth>
# </size>
# <segmented>0</segmented>
# <object>
#   <name>electricity_meter</name>
#   <pose>Unspecified</pose>
#   <truncated>0</truncated>
#   <difficult>0</difficult>
#   <bndbox>
#        <xmin>24</xmin>
#        <ymin>141</ymin>
#       <xmax>569</xmax>
#       <ymax>671</ymax>
#   </bndbox>
# </object>
# <object>
#   <name>counter</name>
#   <pose>Unspecified</pose>
#   <truncated>0</truncated>
#   <difficult>0</difficult>
#   <bndbox>
#       <xmin>150</xmin>
#       <ymin>300</ymin>
#       <xmax>447</xmax>
#       <ymax>347</ymax>
#   </bndbox>
# </object>
# </annotation>
