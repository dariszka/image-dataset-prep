import numpy as np
from PIL import Image

def to_grayscale(pil_image: np.ndarray) -> np.ndarray:

    image = pil_image.copy() 
    if image.ndim == 2:
        img = np.expand_dims(pil_image, axis=0)
        return img
    elif pil_image.ndim == 3:
        pass
    else:
        raise ValueError

if __name__ == "__main__":

    image_path = "2/04_images/gray.png"
    
    with Image.open(image_path) as im:
        image_arr = np.array(im)
        
        greyscale_image = to_grayscale(image_arr)
        img = Image.fromarray(image_arr, mode=im.mode)
        img.show()
