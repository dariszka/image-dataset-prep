import numpy as np
from PIL import Image

def to_grayscale(pil_image: np.ndarray) -> np.ndarray:

    image = pil_image.copy() 
    if image.ndim == 2:
        img = np.expand_dims(pil_image, axis=0)
        return img
    elif pil_image.ndim == 3:
        if image.shape[2] != 3:
            raise ValueError
        else:
            c = image/255 # normalized 
            c_linear = np.where(c <= 0.04045, c/12.92, (((c+0.055)/1.055)**2.4))
            
            y_linear = (c_linear[..., 0] * 0.2126 +
                    c_linear[..., 1] * 0.7152 +
                    c_linear[..., 2] * 0.0722)
            
            y = np.where(y_linear <= 0.0031308, 12.92*y_linear, 1.055*(y_linear**(1/2.4))-0.055)

            if np.issubdtype(image.dtype, np.integer): # denormalized
                y_denormalized = np.round(y * 255)
            else:
                y_denormalized = y * 255
                
            y_denormalized = y_denormalized.astype(image.dtype)
            img = np.expand_dims(y_denormalized, axis=0)

            return img   
    else:
        raise ValueError

if __name__ == "__main__":

    image_path = "2/04_images/gray.png"
    
    with Image.open(image_path) as im:
        image_arr = np.array(im)
        
        greyscale_image = to_grayscale(image_arr)
        img = Image.fromarray(greyscale_image.squeeze(), mode='L')
        img.show()
