from PIL import Image
import glob
import sys


if __name__ == '__main__':
    source_directory = sys.argv[1]
    target_directory = sys.argv[2]
    cuts_number = int(sys.argv[3])
    image_list=[]
    for filename in glob.glob(source_directory + '/*.jpg'):
        im = Image.open(filename)
        image_list.append(im)
    print("------------------------------------------\n")
    print("************{} Images Loaded*************\n".format(len(image_list)))
    print("------------------------------------------\n")

    for image in image_list:
        cropped_image_height = image.height/cuts_number
        cropped_image_width = image.width/cuts_number
        image_name = image.filename.split("/")[-1].replace(".jpg", "")
        for horizontal_cuts in range(0, cuts_number):
            for vertical_cuts in range(0, cuts_number):
                cropped_image = image.crop((vertical_cuts*cropped_image_width, horizontal_cuts*cropped_image_height,vertical_cuts*cropped_image_width + cropped_image_width , horizontal_cuts*cropped_image_height + cropped_image_height))
                cropped_image_name = "{}_{}_{}.jpg".format(target_directory+"/"+image_name,horizontal_cuts, vertical_cuts)
                cropped_image.save(cropped_image_name)