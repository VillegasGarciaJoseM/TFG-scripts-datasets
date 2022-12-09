import argparse

import torch
import torch.backends.cudnn as cudnn
from torchmetrics import PeakSignalNoiseRatio
from torchmetrics import StructuralSimilarityIndexMeasure

import numpy as np
import PIL.Image as pil_image
import glob
from models import SRCNN
from utils import convert_rgb_to_ycbcr, convert_ycbcr_to_rgb, calc_psnr

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights-file', type=str, required=True)
    parser.add_argument('--dataset-file', type=str, required=True)
    parser.add_argument('--scale', type=int, default=3)
    args = parser.parse_args()
    #   Initialize ssim funtion
    ssim_function = StructuralSimilarityIndexMeasure()
    psnr_function = PeakSignalNoiseRatio()

    cudnn.benchmark = True
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    ##  Load model
    model = SRCNN().to(device)

    ##  Load weights and biases
    state_dict = model.state_dict()
    for n, p in torch.load(args.weights_file, map_location=lambda storage, loc: storage).items():
        if n in state_dict.keys():
            state_dict[n].copy_(p)
        else:
            raise KeyError(n)

    model.eval()

    ##  Load images

    ##      Load image names from dataset file
    image_list = glob.glob(args.dataset_file+'/*.png')
    print(image_list.__len__())
    psnr_list = []
    ssim_list = []
    for image_route in image_list:
        image_name = image_route.replace(args.dataset_file, "")

        print('='*5 + "Abriendo imagen " + image_name + '='*(15-image_name.__len__()))
        image = pil_image.open(image_route).convert('RGB')

        print('='*5 + 'Generando imagen lr de ' + image_name + '='*(15-image_name.__len__()))
        image_width = (image.width // args.scale) * args.scale
        image_height = (image.height // args.scale) * args.scale
        image = image.resize((image_width, image_height), resample=pil_image.BICUBIC)
        image = image.resize((image.width // args.scale, image.height // args.scale), resample=pil_image.BICUBIC)
        image = image.resize((image.width * args.scale, image.height * args.scale), resample=pil_image.BICUBIC)


        print('='*5 + 'Obteniendo valores SSIM y PSNR de ' + image_name + '='*(15-image_name.__len__()))
        image = np.array(image).astype(np.float32)
        ycbcr = convert_rgb_to_ycbcr(image)

        y = ycbcr[..., 0]
        y /= 255.
        y = torch.from_numpy(y).to(device)
        y = y.unsqueeze(0).unsqueeze(0)

        with torch.no_grad():
            preds = model(y).clamp(0.0, 1.0)

        preds = preds.mul(255.0).cpu().numpy().squeeze(0).squeeze(0)
        output = np.array([preds, ycbcr[..., 1], ycbcr[..., 2]]).transpose([1, 2, 0])
        output = np.clip(convert_ycbcr_to_rgb(output), 0.0, 255.0).astype(np.uint8)
        output = pil_image.fromarray(output)
        output.save(args.dataset_file+"results/"+image_name.replace('.', '_srcnn_x{}.'.format(args.scale)))

