import os 
import argparse
import json
import glob
import tqdm

CLASSES = ['Car', 'Pedestrian', 'Cyclist', 'Tram', 'Tricycle', 'Truck']


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_root', type=str, )
    config = parser.parse_args()

    json_fps = glob.glob(os.path.join(config.dataset_root, "*.json"))
    classes = set()
    Hs = set()
    Vs = set()
    idx = 0
    
    for ann_fp in tqdm.tqdm(json_fps):
        ann = json.load(open(ann_fp, 'rb'))
        for shape in ann['shapes']:
            classes.add(shape['label'])
            idx += 1
        Hs.add(ann['imageHeight'])
        Vs.add(ann['imageWidth'])
    
    print(f"Based on {idx} labels")
    print(f"Classes in CLASSES: {all([c in CLASSES for c in classes])}")
    print(f"Hs {len(Hs)} and Vs {len(Vs)}")
    
    print(classes)
    print(Hs)
    print(Vs)

    
