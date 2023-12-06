import os 
import argparse
import json
import glob
import tqdm

CLASSES = ['Car', 'Pedestrian', 'Cyclist', 'Tram', 'Tricycle', 'Truck']
CONDITIONS = ['day', 'night']
SUBSETS = ['train', 'val', 'test']
PROPORTIONS = [.8, .1, .1]
OUT_DIR = "out"

import random
random.seed(11)

from itertools import accumulate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_root', type=str, )
    config = parser.parse_args()

    for condition in CONDITIONS:
        fps = glob.glob(os.path.join(config.dataset_root, f"{condition}-*.raw"))
        random.shuffle(fps)	
        L = len(fps)
        split_idxs = list(accumulate([int(p*L) for p in PROPORTIONS]))
        split_idxs = [0, ]+[i+(L-split_idxs[-1]) for i in split_idxs]
        for subset, idx0, idx1 in zip(SUBSETS, split_idxs[:-1], split_idxs[1:]):
            out_fp = os.path.join(OUT_DIR, f"{condition}-{subset}.txt")
            with open(out_fp, 'w') as text_file:
                for fp in fps[idx0:idx1]:
                    _, fn = os.path.split(fp)
                    text_file.write(fn + '\n')
        