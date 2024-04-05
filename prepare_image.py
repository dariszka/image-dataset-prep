import numpy as np
from PIL import Image

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
        pass
        # Pad the image to the desired shape by equally adding pixels to the start and end 
        # of that dimension. The pad-pixel used should be the same as the previous border. 
        # If an unequal amount of padding needs to be added, add the additional pixel to the end
    elif og_width > width: #crop
        
        diff = og_width - width
        if diff%2 == 0:
            start = int(diff/2)
            end = int(start + width)
            resized_image = image_c[:, :, start:end] 
        else:
            start = round(diff/2) # 0.5 will round up to 1
            end = int(start + width)
            resized_image = image_c[:, :, start:end] 
    else:
        resized_image = image_c

# handle height of resized image

    if og_height < height: #pad
        pass
    elif og_height > height: #crop
        diff = og_height - height
        if diff%2 == 0:
            start = int(diff/2)
            end = int(start + height)
            resized_image = resized_image[:, start:end, :] 
        else:
            start = round(diff/2)
            end = int(start + height)
            resized_image = resized_image[:, start:end, :] 
    

    resized_image = resized_image.astype(image.dtype)
    subarea = None

    return (resized_image, subarea)

if __name__ == "__main__":

    image_path = "flower.jpg"
    
    with Image.open(image_path) as im:
        image_arr = np.array(im)

        img = np.expand_dims(image_arr, axis=0)
        prepared_image = prepare_image(img,505,505,300,300,150)
        for image in prepared_image:
            try:
                img = Image.fromarray(image.squeeze(), mode='L') 
                img.show() 
            except:
                pass
        
