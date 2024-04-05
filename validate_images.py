import glob
import os

from PIL import Image
import numpy as np

import hashlib

import csv
import shutil

def validate_images(input_dir: str, output_dir: str,
                    log_file: str, formatter: str = "07d"):

# handle input dir
    input_dir = os.path.abspath(input_dir)
    parent_dir = os.path.dirname(input_dir)

    if os.path.isdir(input_dir):
        paths = []
        for f in glob.glob(f'{input_dir}/**', recursive=True):
            if os.path.isfile(f):
                paths.append(f)
        paths.sort()
    else:
        raise ValueError('input_dir is not an existing directory')

# handle output dir

    if not os.path.isabs(output_dir):
        output_dir = os.path.join(parent_dir, output_dir) # if abspath not specified, I'm defaulting to same dir as input
    os.makedirs(output_dir, exist_ok=True)

# handle log file

    if not os.path.isabs(log_file):
        log_file = os.path.join(parent_dir, log_file) 

    try:
    # opening it in write mode once in the beginning to create new 
        with open(log_file, mode='w', newline='\n') as file:
            pass
    except FileNotFoundError: #if missing intermediate directories
        log_file_parent = os.path.dirname(log_file)
        os.makedirs(log_file_parent, exist_ok=True)
        with open(log_file, mode='w', newline='\n') as file:
            pass

# 1. The file name ends with .jpg, .JPG, .jpeg or .JPEG.

    # https://stackoverflow.com/questions/18351951/check-if-string-ends-with-one-of-the-strings-from-a-list
    # used this
    images1 = []
    extensions_list = ['.jpg', '.JPG', '.jpeg', '.JPEG']
    for path in paths:
        if os.path.splitext(path)[-1] in extensions_list:
            images1.append(path)
        else:
            relpath = os.path.relpath(path, input_dir)
            with open(log_file, mode='a', newline='') as file:
                file.write(f'{relpath},1\n')

# 2. The file size does not exceed 250kB (=250 000 Bytes).
    images2 = []
    for image in images1:
        size = os.path.getsize(image)
        if size <= 250000:
            images2.append(image)
        else:
            relpath = os.path.relpath(image, input_dir)
            with open(log_file, mode='a', newline='') as file:
                file.write(f'{relpath},2\n')

# 3. The file can be read as image (i.e., the PIL/pillow module does not raise an exception
    # when reading the file).
    images3 = []
    for image in images2:
            try:
                with Image.open(image) as img:
                    images3.append(image)
            except:
                relpath = os.path.relpath(image, input_dir)
                with open(log_file, mode='a', newline='') as file:
                    file.write(f'{relpath},3\n')
           
# 4. The image data has a shape of (H, W, 3) with H (height) and W (width) larger than or
    # equal to 100 pixels, and the three channels must be in the order RGB (red, green, blue).
    # Alternatively, the image can also be grayscale and have a shape of only (H, W) with the
    # same width and height restrictions.
    
    images4 = []
    for image in images3:
        with Image.open(image) as im:
            img = np.array(im)
            if im.mode == 'RGB' and img.ndim == 3:
                    if img.shape[0] >= 100 and img.shape[1] >= 100:
                        images4.append(image)
                    else:    
                        relpath = os.path.relpath(image, input_dir)
                        with open(log_file, mode='a', newline='') as file:
                            file.write(f'{relpath},4\n')
            elif im.mode == 'L' and img.ndim == 2:
                    if img.shape[0] >= 100 and img.shape[1] >= 100:
                        images4.append(image) 
                    else:
                        relpath = os.path.relpath(image, input_dir)
                        with open(log_file, mode='a', newline='') as file:
                            file.write(f'{relpath},4\n')
            else:    
                relpath = os.path.relpath(image, input_dir)
                with open(log_file, mode='a', newline='') as file:
                    file.write(f'{relpath},4\n')
                    
            
# 5. The image data has a variance larger than 0, i.e., there is not just one common pixel in
    # the image data.
    images5 = []
    for image in images4:
        with Image.open(image) as im:
            img = np.array(im)
            if np.var(img) > 0:
                images5.append(image)
            else:
                relpath = os.path.relpath(image, input_dir)
                with open(log_file, mode='a', newline='') as file:
                    file.write(f'{relpath},5\n')

# 6. The same image has not been copied already.

    images6 = []
    array_hashes = set()

    for image in images5:
        with Image.open(image) as im:
            img = np.array(im) 
            img_bytes = img.tobytes() 
            hashing_object = hashlib.sha256()
            hashing_object.update(img_bytes)
            array_digest = hashing_object.digest()

            if array_digest not in array_hashes:
                images6.append(image)
                array_hashes.add(array_digest)
            else:
                relpath = os.path.relpath(image, input_dir)
                with open(log_file, mode='a', newline='') as file:
                    file.write(f'{relpath},6\n')

# handle labels and copying

    csv_file_path = f'{output_dir}/labels.csv'

    # https://pythonspot.com/files-spreadsheets-csv/
    with open(csv_file_path, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['name', 'label'])

    for i, image in enumerate(images6):

        # https://codeigo.com/python/copy-and-rename-files-python/ used this

        basename = os.path.basename(image)
        filename, _ = os.path.splitext(basename)

        # https://stackoverflow.com/questions/12851791/removing-numbers-from-string
        filename = ''.join([i for i in filename if i.isalpha()])

        new_name = "{:{}}.jpg".format(i, formatter)
        output_file = os.path.join(output_dir, new_name)

        with open(csv_file_path, 'a', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow([new_name, filename])
  
        shutil.copy(image, output_file)
    
    return len(images6)



