import random
import xml.etree.ElementTree as ET
import os
from tqdm import tqdm
import collections


def xml_file_name_labels(root_dir, label_path):
    """
    检查物体的名字是实际名字
    """
    labels = collections.OrderedDict()
    for p in enumerate(label_path):
        for file in os.listdir(os.path.join(root_dir, p)):
            root = ET.parse(os.path.join(root_dir, p, file)).getroot()
            objects = root.findall('object')
            for object in objects:
                name = object.find('name').text
                if name in labels.keys():
                    continue
                else:
                    labels[name] = len(labels)
    return labels


def xml_file_name(root_dir, label_path, img_path, types, labels):
    """
    label是单独的xml文件, 检查物体的名字是实际名字
    """
    output_dir = 'images'  # 不能改成别的,训练时会报错
    for i in types:
        if not os.path.exists(os.path.join(root_dir, 'labels', i)):
            os.makedirs(os.path.join(root_dir, 'labels', i))
    for i in types:
        if not os.path.exists(os.path.join(root_dir, output_dir, i)):
            os.makedirs(os.path.join(root_dir, output_dir, i))

    for index, p in enumerate(label_path):
        for file in os.listdir(os.path.join(root_dir, p)):
            if not file.endswith('.xml'):
                continue
            try:
                root = ET.parse(os.path.join(root_dir, p, file)).getroot()
            except:
                print('读取失败', os.path.join(root_dir, img_path[index], filename))
                continue
            filename = root.find('filename').text
            file_path = os.path.join(root_dir, img_path[index], filename)
            file_to_path = os.path.join(root_dir, output_dir, types[index], filename)
            try:
                os.rename(file_path, file_to_path)
            except:
                continue
            objects = root.findall('object')
            width = int((root.find('size').find('width')).text)
            height = int((root.find('size').find('height')).text)
            label = open(os.path.join(root_dir, 'labels', types[index], filename.split('.')[0] + '.txt'), 'w')
            for object in objects:
                name = object.find('name').text
                bndbox = object.find('bndbox')
                xmin = int(bndbox.find('xmin').text) / width
                ymin = int(bndbox.find('ymin').text) / height
                xmax = int(bndbox.find('xmax').text) / width
                ymax = int(bndbox.find('ymax').text) / height

                # x_center y_center width height
                label.write(str(labels[name]) + ' ' + str(((xmin + xmax) / 2)) + ' ' +
                            str(((ymin + ymax)) / 2) + ' ' + str(xmax - xmin) + ' ' + str(ymax - ymin) + '\n')
            label.close()

    with open(os.path.join(root_dir, 'data.yaml'), 'w') as f:
        for index, i in enumerate(types):
            f.write(f'{i}: {os.path.join(root_dir, output_dir, types[index])} \n')
        f.write(f'\n\n')
        f.write('names:\n')
        for k, v in labels.items():
            f.write(f" {v}: {k}\n")


def voc_to_yolo(root_dir, label_path, img_path, types, labels, split=None):
    """
    label是单独的xml文件, 检查物体的名字是实际名字
    """

    output_dir = 'images'  # 不能改成别的,训练时会报错

    for i in types:
        if not os.path.exists(os.path.join(root_dir, 'labels', i)):
            os.makedirs(os.path.join(root_dir, 'labels', i))
    for i in types:
        if not os.path.exists(os.path.join(root_dir, output_dir, i)):
            os.makedirs(os.path.join(root_dir, output_dir, i))
    if split is not None and len(types) == 1:
        os.makedirs(os.path.join(root_dir, 'labels', 'val'))
        os.makedirs(os.path.join(root_dir, output_dir, 'val'))
    for index, p in enumerate(label_path):
        for file in os.listdir(os.path.join(root_dir, p)):
            t = types[index]
            if split is not None and len(types) == 1:
                if random.randint(0, 100) < split:
                    t = 'val'
            else:
                is_val = False
            if not file.endswith('.xml'):
                continue
            try:
                root = ET.parse(os.path.join(root_dir, p, file)).getroot()
            except:
                print('读取失败', os.path.join(root_dir, img_path[index], file))
                continue
            # filename = root.find('filename').text
            path = root.find('path').text
            if "\\" in path:
                filename = path.split("\\")[-1]
            elif "/" in path:
                filename = path.split("/")[-1]
            file_path = os.path.join(root_dir, img_path[index], filename)
            file_to_path = os.path.join(root_dir, output_dir, t, filename)
            try:
                os.rename(file_path, file_to_path)
                ...
            except Exception as e:
                # print(e)
                continue
            objects = root.findall('object')
            width = int((root.find('size').find('width')).text)
            height = int((root.find('size').find('height')).text)
            label = open(os.path.join(root_dir, 'labels', t, filename.split('.')[0] + '.txt'), 'w')
            # print(filename)
            for object in objects:
                name = object.find('name').text
                bndbox = object.find('bndbox')
                xmin = int(bndbox.find('xmin').text) / width
                ymin = int(bndbox.find('ymin').text) / height
                xmax = int(bndbox.find('xmax').text) / width
                ymax = int(bndbox.find('ymax').text) / height

                # x_center y_center width height
                label.write(name + ' ' + str(((xmin + xmax) / 2)) + ' ' +
                            str(((ymin + ymax)) / 2) + ' ' + str(xmax - xmin) + ' ' + str(ymax - ymin) + '\n')
            label.close()

    with open(os.path.join(root_dir, 'data.yaml'), 'w') as f:
        for index, i in enumerate(types):
            f.write(f'{i}: {os.path.join(root_dir, output_dir, types[index])} \n')
        if split is not None and len(types) == 1:
            f.write(f'val: {os.path.join(root_dir, output_dir, "val")} \n')

        f.write(f'\n\n')
        f.write('names:\n')
        for k, v in labels.items():
            f.write(f" {v}: {k}\n")

    
    


if __name__ == '__main__':
    # root_dir = r'C:\Users\xingshuyin\Downloads\insects\data\insects'
    # label_path = [r"train\annotations\xmls", r"val\annotations\xmls", r"test\annotations\xmls"]
    # img_path = [r"train\images", r"val\images", r"test\images"]
    # types = ['train', 'val', 'test']
    # labels = xml_file_name_labels(root_dir, label_path)
    # xml_file_name(root_dir, label_path, img_path, types, labels)

    # root_dir = r'C:\Users\xingshuyin\python\datasets\VOC2007'
    # label_path = [r"Annotations"]
    # img_path = [r"JPEGImages"]
    # types = ['train']
    # labels = collections.OrderedDict()
    # with open(r"C:\Users\xingshuyin\python\datasets\病虫害\classes.txt", 'r') as f:
    #     for index, i in enumerate(f.readlines()):
    #         labels['_'.join(i.split()[1:])] = index
    # voc_to_yolo(root_dir, label_path, img_path, types, labels, 15)
