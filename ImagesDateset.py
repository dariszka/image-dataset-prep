from torch.utils.data import Dataset
from typing import Optional
import numpy as np
import os

class ImagesDataset(Dataset):
    def __init__(
        self,
        image_dir,
        width: int = 100,
        height: int = 100,
        dtype: Optional[type] = None
        ):

        if width < 100 or height < 100:
            raise ValueError
        
        self.image_dir = image_dir
        self.width = width
        self.height = height
        self.dtype = dtype

        found_files = []
        for path in os.listdir(image_dir):
            if os.path.splitext(path)[-1]=='.jpg':
                found_files.append(os.path.abspath(os.path.join(image_dir, path)))
            elif os.path.splitext(path)[-1]=='.csv':
                csv_file = os.path.abspath(os.path.join(image_dir, path))

        found_files.sort()
        self.found_files = found_files

        print(csv_file)
    
        csv_contents = np.genfromtxt(csv_file, delimiter=';', dtype=str, skip_header=1)
        csv_contents = csv_contents[csv_contents[:, 1].argsort()]

        classnames = csv_contents[:,1]
        classnames = classnames.tolist()

        classids = csv_contents[:,0]
        classids = classids.tolist()

        self.classnames = classnames
        self.classids = classids        

    def __getitem__(self, index):
        pass
    def __len__(self):
        return len(self.found_files)
        

dataset = ImagesDataset("./validated_images", 100, 100, int)

# for resized_image, classid, classname, _ in dataset:
#     print(f'image shape: {resized_image.shape}, dtype: {resized_image.dtype}, '
#     f'classid: {classid}, classname: {classname}\n')