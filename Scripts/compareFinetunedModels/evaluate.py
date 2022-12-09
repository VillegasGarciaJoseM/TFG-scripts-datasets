import numpy as np
from skimage.metrics import structural_similarity, peak_signal_noise_ratio
import sys
from skimage import io, color, filters
import os


def rmetrics(a, b):
    psnr=peak_signal_noise_ratio(a,b)

    # ssim
    ssim = structural_similarity(a, b, multichannel=True)

    return psnr, ssim

def main():
    result_path = sys.argv[1]
    reference_path = sys.argv[2]

    result_dirs = os.listdir(result_path)

    sumpsnr, sumssim, sumuiqm, sumuciqe = 0., 0., 0., 0.

    N = 0
    for imgdir in result_dirs:
        if '.png' in imgdir or '.jpg' in imgdir:
            # corrected image
            corrected = io.imread(os.path.join(result_path, imgdir))

            # reference image
            imgname = imgdir.split('corrected')[0]
            imgname = imgname.replace("_srcnn_x4", "")
            imgname = imgname.replace("_ESRGAN_SRx4_DF2KOST_test_150f", "")
            imgname = imgname.replace("_SwinIR_SRx4_TFG_ALOT", "")
            imgname = imgname.replace(".png", ".jpg")
            refdir = imgname.replace("_SwinIR_SRx4_TFG_official", "")

            reference = io.imread(os.path.join(reference_path, refdir))

            psnr, ssim = rmetrics(corrected, reference)


            sumpsnr += psnr
            sumssim += ssim
            N += 1

            with open(os.path.join(result_path, 'metrics.txt'), 'a') as f:
                f.write('{}: psnr={} ssim={}\n'.format(imgname, psnr, ssim))

    mpsnr = sumpsnr / N
    mssim = sumssim / N

    with open(os.path.join(result_path, 'metrics.txt'), 'a') as f:
        f.write('Average: psnr={} ssim={}\n'.format(mpsnr, mssim))

if __name__ == '__main__':
    main()
