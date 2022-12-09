import argparse
import glob
import PIL.Image as pil_image
import os
import shutil
import random
from operator import itemgetter

def extractImages(args):
    dataset_path = args.folder
    num_images = args.num_images
    dst_path = args.dst_folder

    subfolders = [f.path for f in os.scandir(dataset_path) if f.is_dir()]

    for folder in subfolders:
        n_images = random.choices(os.listdir(folder), k=num_images)
        for image in n_images:
            print("{}/{}".format(folder, image))
            shutil.copy("{}/{}".format(folder, image), dst_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, required=True)
    parser.add_argument('--num-images', type=int, required=True)
    parser.add_argument('--dst-folder', type=str, default='/home/josele/datasets/ALOT/ALOT-reduced')

    args = parser.parse_args()

    extractImages(args)