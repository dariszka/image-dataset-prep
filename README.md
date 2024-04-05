# ds_prep

to_grayscale converts a pil_image (expected to be the raw data of an image loaded with Pillow) 
to grayscale using the colorimetric conversion. The conversion works on an RGB input image where 
all values have been normalized to the range [0, 1] before the (also normalized) grayscale output Y 
is calculated.

The function returns the denormalized grayscale-converted image including a dedicated channel
for the brightness information in the 3D shape: (1, H, W), where H is the height and W
the width of the image. The specified pil_image is handled as follows:
•   If the image has a 2D shape, it is assumed to already be a grayscale image with shape (H, W),
and a copy with shape (1, H, W) is returned.
•   If the image has a 3D shape, it is assumed to be (H, W, 3), i.e., the third dimension represents
the RGB channels (in the order R, G and B, which can also be assumed to be true). 
•   Assumption that the images passed to the function will only have values within the range
[0, 255]. Easy normalization by dividing all image values by 255. The original input image is not be 
changed, i.e., the normalization and grayscale conversion is done on a copy. 
•   The data type of the image can be arbitrary. If it is an np.integer (use np.issubdtype), then
rounding (to zero decimals) is applied before returning the grayscale-converted image.
The returned grayscale-converted image has the same data type as the input image.
