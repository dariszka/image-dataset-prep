# ds_prep

Programming in Python 2 Assignments.

## validate_images

validates images as follows:
+ input_dir specifies the input directory where the function recursively looks for files, 
sorted in ascending order according to their file names. If input_dir is not an existing 
directory, a ValueError is raised.
+ output_dir specifies the directory where all valid images (from the sorted list of files above)
are copied to. If the directory does not exist, it is created. 
+ Image files are considered valid if the following rules are met:
> > 1. The file name ends with .jpg, .JPG, .jpeg or .JPEG.
> > 2. The file size does not exceed 250kB (=250 000 Bytes).
> > 3. The file can be read as image (i.e., the PIL/pillow module does not raise an exception
when reading the file).
> > 4. The image data has a shape of (H, W, 3) with H (height) and W (width) larger than or
equal to 100 pixels, and the three channels must be in the order RGB (red, green, blue).
Alternatively, the image can also be grayscale and have a shape of only (H, W) with the
same width and height restrictions.
> > 5. The image data has a variance larger than 0, i.e., there is not just one common pixel in
the image data.
> > 6. The same image has not been copied already.

+ The base name (without any extension) of the copied file is as defined by the format
string formatter, which expects a single number that is used to apply the format
string on. The number is an integer starting at 0, and it is incremented by 1 for every
file that has been copied. The extension of every copied file is .jpg. Example:

– Input files:
∗ cat.jpeg (valid)
∗ dog2.png (invalid)
∗ tree1.jpg (valid)
∗ tree2.JPG (valid)

– Format string: "07d"
– Output image files:
∗ 0000000.jpg (from cat.jpeg)
∗ 0000001.jpg (from tree1.jpg)
∗ 0000002.jpg (from tree2.JPG)

+ In order to retain the label for each image, the new file name and the corresponding label are
written to a csv file (file name: labels.csv), where the first column is the file name
and the second column the corresponding label (headers: name and label), like this:
name;label
0000000.jpg;cat
0000001.jpg;tree
0000002.jpg;tree
0000003.jpg;car
0000004.jpg;cat
...

+ log_file specifies the path of the log file to which file names of invalid files must be written.
The format of log_file is as follows:
> > 1. Each line contains the file name of the invalid file, followed by a comma, an error
code and a newline character.
> > 2. The error code is an integer with 1 digit, corresponding to the list of rules for file validity
from above (i.e., there are a total of 6 error codes). Only one error code per file is
written, and the rules are checked in the ascending order 1, 2, 3, 4, 5, 6.
> > 3. Each file name only contains the relative file path starting from input_dir (input_dir itself is 
not part of the relative path anymore).
For the example from above, the log file should contain the following line (with a trailing
newline character):
dog2.png,1
> > 4. The log file is always newly created (even if it already exists), and potentially missing inter-
mediate directories are also created.

+ formatter specifies an optional format string to use when writing the output images. It
expects a single number that is used to apply the format string on (e.g., with the default value
of "07d", the result should be the same as "{:07d}".format(some_number)). The result is
the base name of the file, without any extension.

+ The function must return the number of valid files that were copied as integer. In the example
above, 3 would be returned.


## to_grayscale 
converts a pil_image (expected to be the raw data of an image loaded with Pillow) 
to grayscale using the colorimetric conversion. The conversion works on an RGB input image where 
all values have been normalized to the range [0, 1] before the (also normalized) grayscale output Y 
is calculated.

The function returns the denormalized grayscale-converted image including a dedicated channel
for the brightness information in the 3D shape: (1, H, W), where H is the height and W
the width of the image. The specified pil_image is handled as follows:
+   If the image has a 2D shape, it is assumed to already be a grayscale image with shape (H, W),
and a copy with shape (1, H, W) is returned.
+   If the image has a 3D shape, it is assumed to be (H, W, 3), i.e., the third dimension represents
the RGB channels (in the order R, G and B, which can also be assumed to be true). 
+   Assumption that the images passed to the function will only have values within the range
[0, 255]. Easy normalization by dividing all image values by 255. The original input image is not be 
changed, i.e., the normalization and grayscale conversion is done on a copy. 
+   The data type of the image can be arbitrary. If it is an np.integer (use np.issubdtype), then
rounding (to zero decimals) is applied before returning the grayscale-converted image.
The returned grayscale-converted image has the same data type as the input image.


## prepare_image
prepares an image for the classification machine learning project. Its main task is to resize
the given image by padding and cropping it, and also to return a subarea that is specified via the
parameters x, y and size. All parameters are explained in the following:
+ image is a 3D NumPy array with shape (1, H, W) that contains a grayscale image. This
image is resized and cropped according to the remaining parameters.
+ width specifies the width of the resulting image.
+ height specifies the height of the resulting image.
+ x specifies the x-coordinate within resized_image where the subarea should start.
+ y specifies the y-coordinate within resized_image where the subarea should start.
+ size specifies the size in both dimensions of the cropped subarea.

> The resizing process works as follows:
+ If the input image is smaller in width or height than width or height respectively, pads the
image to the desired shape by equally adding pixels to the start and end of that dimension. The
pad-pixel is the same as the previous border. If an unequal amount of padding
needs to be added, adds the additional pixel to the end.
+ If the input image is larger in width or height than width or height respectively, crops the
image to the desired shape by cutting out an equal amount of the bordering pixels in both
dimensions. If an unequal amount of pixels have to be cut, breaks the tie by first cutting pixels
at the start of the dimension.
+ In addition, a smaller, square subarea of the resized image is returned. x and y specify the
start of the subarea with size specifying the length in both dimensions.

> The function returns the 2-tuple (resized_image, subarea):
+ resized_image is the 3D NumPy array that represents the resized version of the input image.
The array is a copy, i.e., the original input image is not changed. It has
the same data type as the input image and shape (1, height, width).
+ subarea is a 3D NumPy array that represents a subarea of pixels according to the other
parameters. It has the same data type as the input image and shape (1, size, size)

The function handles various error cases. Specifically, it raises a ValueError in the
following cases:
+ The shape of image is not 3D or the channel size is not exactly 1 (i.e., shape (1, H, W)).
+ Either width, height or size are smaller than 32.
+ x is smaller than 0 or x + size is larger than the width of the resized image, i.e., the subarea
would exceed the resized image width.
+ y is smaller than 0 or y + size is larger than the height of the resized image, i.e., the subarea
would exceed the resized image height.