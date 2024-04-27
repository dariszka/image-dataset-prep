from torch.utils.data import Dataset, DataLoader
from ImagesDateset import ImagesDataset

def stacking(batch_as_list: list): 
    pass

ds = ImagesDataset("./validated_images", 100, 100, int)
dl = DataLoader(ds, batch_size=2, shuffle=False, collate_fn=stacking)
for i, (images, classids, classnames, image_filepaths) in enumerate(dl):
    print(f'mini batch: {i}')
    print(f'images shape: {images.shape}')
    print(f'class ids: {classids}')
    print(f'class names: {classnames}\n')