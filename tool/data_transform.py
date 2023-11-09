import xml.etree.ElementTree as ET
import os


def xml():
    """
    label是单独的xml文件
    """
    root_dir = r'C:\Users\xingshuyin\Downloads\insects\data\insects'
    label_path = [r"train\annotations\xmls", r"val\annotations\xmls", r"test\annotations\xmls"]
    img_path = [r"train\images", r"val\images", r"test\images"]
    types = ['train', 'val', 'test']  # ['train', 'val', 'test']
    labels = {}
    output_dir = 'images'  # 不能改成别的,训练时会报错
    for index, p in enumerate(label_path):
        for file in os.listdir(os.path.join(root_dir, p)):
            root = ET.parse(os.path.join(root_dir, p, file)).getroot()
            filename = root.find('filename').text
            objects = root.findall('object')
            for object in objects:
                name = object.find('name').text
                if name in labels.keys():
                    continue
                else:
                    labels[name] = len(labels)

    for i in types:
        if not os.path.exists(os.path.join(root_dir, 'labels', i)):
            os.makedirs(os.path.join(root_dir, 'labels', i))
    for i in types:
        if not os.path.exists(os.path.join(root_dir, output_dir, i)):
            os.makedirs(os.path.join(root_dir, output_dir, i))

    for index, p in enumerate(label_path):
        for file in os.listdir(os.path.join(root_dir, p)):
            root = ET.parse(os.path.join(root_dir, p, file)).getroot()
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
            print(filename)
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
