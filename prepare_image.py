import numpy as np
from PIL import Image

def prepare_image(image: np.ndarray,
                    width: int,
                    height: int,
                    x: int,
                    y: int,
                    size: int
                    ) -> tuple[np.ndarray, np.ndarray]:
    
    # handle errors
    if image.ndim != 3 or image.shape[0] != 1:
        raise ValueError
    
    if width < 32 or height < 32 or size < 32:
        raise ValueError
    
    if x < 0 or (x+size) > width:
        raise ValueError

    if y < 0 or (y+size) > height:
        raise ValueError
    

    resized_image = None
    subarea = None

    return (resized_image, subarea)

if __name__ == "__main__":

    image_path = "flower.jpg"
    
    with Image.open(image_path) as im:
        image_arr = np.array(im)

        img = np.expand_dims(image_arr, axis=0)
        prepared_image = prepare_image(img,500,500,300,300,150)
        
