import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def prepare_image(image: np.ndarray,
                    width: int,
                    height: int,
                    x: int,
                    y: int,
                    size: int
                    ) -> tuple[np.ndarray, np.ndarray]:
    image_c = image.copy() 

# handle errors
    if image_c.ndim != 3 or image_c.shape[0] != 1:
        raise ValueError
    
    if width < 32 or height < 32 or size < 32:
        raise ValueError
    
    if x < 0 or (x+size) > width:
        raise ValueError

    if y < 0 or (y+size) > height:
        raise ValueError
    
    og_height = image_c.shape[1]
    og_width = image_c.shape[2]

# handle width of resized image
    if og_width < width: #pad
        diff = width - og_width
        pad_val = int(diff/2)
        if diff%2==0:
            resized_image = np.pad(image_c, pad_width=((0,0), (0,0), (pad_val,pad_val)), mode='edge')
        else:
            resized_image = np.pad(image_c, pad_width=((0,0), (0,0), (pad_val,pad_val+1)), mode='edge')
    elif og_width > width: #crop
        diff = og_width - width
        if diff%2 == 0:
            start = int(diff/2)
            end = int(start + width)
            resized_image = image_c[:, :, start:end] 
        else:
            start = int(diff/2) + 1
            end = int(start + width)
            resized_image = image_c[:, :, start:end] 
    else:
        resized_image = image_c

# handle height of resized image
    if og_height < height: #pad
        diff = height - og_height
        pad_val = int(diff/2)
        if diff%2==0:
            resized_image = np.pad(resized_image, pad_width=((0,0), (pad_val,pad_val), (0,0)), mode='edge')
        else:
            resized_image = np.pad(resized_image, pad_width=((0,0), (pad_val,pad_val+1), (0,0)), mode='edge')
    elif og_height > height: #crop
        diff = og_height - height
        if diff%2 == 0:
            start = int(diff/2)
            end = int(start + height)
            resized_image = resized_image[:, start:end, :] 
        else:
            start = int(diff/2) + 1
            end = int(start + height)
            resized_image = resized_image[:, start:end, :] 
    
# handle subarea
    subarea = resized_image[:, y:(y+size), x:(x+size)] # y is height, x is width

# cast to original dtype 
    resized_image = resized_image.astype(image.dtype)
    subarea = subarea.astype(image.dtype)

    return (resized_image, subarea)

if __name__ == "__main__":

    image_path = "flower.jpg"
    
    with Image.open(image_path) as im:
        image_arr = np.array(im)

        img = np.expand_dims(image_arr, axis=0)
        prepared_image = prepare_image(img,600,600,400,400,150)
        
        img = Image.fromarray(prepared_image[1].squeeze(), mode='L') 
        img.show() 
