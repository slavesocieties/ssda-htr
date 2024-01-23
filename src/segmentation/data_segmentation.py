import os
from PIL import Image, ImageOps
from deslant_img import *


def data_segmentation(data, crop_pixels, file_name, image_file, start_id, coords = []):
    """Function to crop input image by lines and output cropped images as specified by pixel boundaries
    The resulting images will be saved to disk in the segmented directory

    Parameters
    ----------
    data : numpy array
        rotated image as a numpy array
    crop_pixels array : list
        of indices indicate where to crop the image
    file_name : string
        name of the root file
    image_file : Image
        the gray-scale version of the image file object to be cropped        
    start_id : int
        id of the current starting line
    coords : list
        coordinates of block in original image

    Returns
    -------
    count : int
        number of saved segments
    segment_coords : list
        a list of coordinates of saved segments
    """
    #establising initial boundaries
    top = 0
    left = 0
    right = data.shape[1]
    bottom = 0
    index = 0

    count = 0

    segment_coords = []

    if not os.path.exists("./segmented"):
        os.mkdir("./segmented")

    if not os.path.exists("./segmented/"+file_name):
        os.mkdir("./segmented/"+file_name)

    while index < len(crop_pixels): #iteratively crop the image with pixel boundaries
        top = bottom
        bottom = crop_pixels[index]

        # remove strips that are too small
        # this will likely eventually need to be tweaked for each volume/group of volumes
        while bottom - top < 10:
            index += 1
            if index >= len(crop_pixels):
                return count, segment_coords, start_id
            # left = bottom
            top = bottom
            bottom = crop_pixels[index]
      
        tmp_img = image_file.crop((left, top, right, bottom))

        #deslanting
        tmp_img = deslant_img(np.array(tmp_img))
        tmp_img = Image.fromarray(tmp_img.img)

        idx = ''
        if start_id < 10:
            idx = '0'+str(start_id)
        else:
            idx = str(start_id)

        tmp_img.save("./segmented/"+file_name+"/"+file_name+'-'+idx+'.jpg') #save output image
        segment_coords.append([left + coords[0], top + coords[1], right + coords[0], bottom + coords[1]])
        count += 1
        start_id +=1

        index+=1
    # image_file = image_file.crop((top, bottom, right, data.shape[0]))
    image_file = image_file.crop((left, bottom, right, data.shape[0]))

    # image_file = deslant_img(np.array(image_file))
    # image_file = Image.fromarray(image_file.img)

    
    idx = ''
    if start_id < 10:
        idx = '0'+str(start_id)
    else:
        idx = str(start_id)
    if image_file.size[1] > 9:
        image_file.save("./segmented/" + file_name + "/" + file_name + '-' + idx + '.jpg')  # save output image
        segment_coords.append([left + coords[0], bottom + coords[1], right + coords[0], data.shape[0] + coords[1]])
        count += 1
        start_id += 1
    
    return count, segment_coords, start_id
