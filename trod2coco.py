import os 
import argparse
import json
import glob
import tqdm
import json

CLASSES = ['Pedestrian', 'Cyclist', 'Car', 'Tram', 'Tricycle', 'Truck']
CONDITIONS = ['day', 'night']
SUBSETS = ['train', 'val', 'test']
OUT_DIR = "out"


CATEGORIES = [
    {
        "supercategory": "person",
        "id": 1,
        "name": "Pedestrian"
    },
    {
        "supercategory": "vehicle",
        "id": 2,
        "name": "Cyclist"
    },
    {
        "supercategory": "vehicle",
        "id": 3,
        "name": "Car"
    },
    {
        "supercategory": "vehicle",
        "id": 4,
        "name": "Tram"
    },
    {
        "supercategory": "vehicle",
        "id": 5,
        "name": "Tricycle"
    },
    {
        "supercategory": "vehicle",
        "id": 6,
        "name": "Truck"
    }
]

CLASS2CATEGORY_ID = {d["name"] : d["id"] for d in CATEGORIES}


import random
random.seed(11)

def get_img_info(ann):
    image_info = {
        'file_name':  ann["imagePath"].replace("jpg", "raw"),
        'height': ann['imageHeight'],
        'width': ann['imageWidth'],
        # 'id': ann["imagePath"].split(".")[0]
    }
    return image_info

def get_shape_info(shape):
    category_id = CLASS2CATEGORY_ID[shape['label']]
    (pt0, pt1) = shape['points']
    xmin = min(pt0[0], pt1[0])
    ymin = min(pt0[1], pt1[0])
    xmax = max(pt0[0], pt1[0])
    ymax = max(pt0[1], pt1[0])
    xmin = int(xmin) - 1
    ymin = int(ymin) - 1
    xmax = int(xmax)
    ymax = int(ymax)
    assert xmax > xmin and ymax > ymin, f"Box size error !: (xmin, ymin, xmax, ymax): {xmin, ymin, xmax, ymax}"
    o_width = xmax - xmin
    o_height = ymax - ymin
    ann = {
        'area': o_width * o_height,
        'iscrowd': 0,
        'bbox': [xmin, ymin, o_width, o_height],
        'category_id': category_id,
        'ignore': 0,
        'segmentation': []  # This script is not for segmentation
    }
    return ann

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_root', type=str, )
    parser.add_argument('filelist', type=str, )
    config = parser.parse_args()

    with open(config.filelist, 'r') as file:
        fns = file.readlines()
    fns = [fn.strip() for fn in fns]
    
    output_json_dict = {
        "categories": CATEGORIES,
        "images": [],
        "type": "instances",
        "annotations": [],
    }
    
    _, filelist_fn = os.path.split(config.filelist)
    output_json_fn = ".".join(filelist_fn.split(".")[:-1] + ["json"])
    output_json_fp = os.path.join(OUT_DIR, output_json_fn)
    
    img_id = 1
    bnd_id = 1 # bnding box id    
    for fn in tqdm.tqdm(fns):
        fp = os.path.join(config.dataset_root, fn)
        ann_fp = fp.replace(".raw", ".json")
        ann = json.load(open(ann_fp, 'rb'))
        
        img_info = get_img_info(ann)
        img_info["id"] = img_id
        img_id += 1
        output_json_dict["images"].append(img_info)
        
        for shape in ann['shapes']:
            shape_info = get_shape_info(shape)
            shape_info['image_id'] = img_info["id"]
            shape_info['id'] = bnd_id
            output_json_dict["annotations"].append(shape_info)
            bnd_id += 1
            
    with open(output_json_fp, 'w') as json_file:
        json.dump(output_json_dict, json_file, indent=2)  # 'indent' parameter for pretty formatting (optional)
