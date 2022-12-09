import argparse
import glob
import PIL.Image as pil_image

def downsize(args):

    for image_path in sorted(glob.glob('{}/*.png'.format(args.images_dir))):
        hr = pil_image.open(image_path).convert('RGB')
        hr_width = (hr.width // args.scale) * args.scale
        hr_height = (hr.height // args.scale) * args.scale
        hr = hr.resize((hr_width, hr_height), resample=pil_image.BICUBIC)
        lr = hr.resize((hr_width // args.scale, hr_height // args.scale), resample=pil_image.BICUBIC)

        image_name = image_path.split("/")[-1].replace(".jpg", "")
        image_directory_hr = "{}/{}/{}".format(args.output_path, "hr", image_name)
        image_directory_lr = "{}/{}".format(args.output_path, image_name)
        print(image_directory_lr)
        hr.save(image_directory_hr)
        lr.save(image_directory_lr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images-dir', type=str, required=True)
    parser.add_argument('--output-path', type=str, required=True)
    parser.add_argument('--scale', type=int, default=4)
    args = parser.parse_args()

    downsize(args)