import torch.utils.data
import torch
from scipy.ndimage import imread
import os
import os.path
import glob
from torchvision import transforms
from pathlib import Path
import shutil


class DataPrep(torch.utils.data.Dataset):
    def __init__(self, root, transform, train=True):
        self.root = root
        self.train = train
    
    def __getitem__(self, idx):
        img = imread(img_path)
        img = torch.from_numpy(img).float()

        gt = imread(g_path)
        gt = torch.from_numpy(gt).float()

        return img, gt
    
    def __len__(self):
        return len(self.imagenumber)


def main():
    # https://blog.csdn.net/woshicao11/article/details/82055449
    # https://blog.csdn.net/woshicao11/article/details/78318156
    # https://blog.csdn.net/renelian1572/article/details/78761278
    paver(r"D: \workspace\OnProjects\resnet_wheat\project2\Daata")

def paver(user_data_dir):
    log_dir   = Path.cwd().joinpath("log")
    model_dir = Path.cwd().joinpath("model")
    data_dir  = Path.cwd().joinpath("data")
    train_dir = data_dir.joinpath("train")
    test_dir  = data_dir.joinpath("test")
    for dir_name in [log_dir, model_dir, data_dir]:
        if not Path.exists(dir_name):
            Path.mkdir(dir_name)
    user_data_dir = Path(user_data_dir.replace(" ", ""))
    if not train_dir.exists() and test_dir.exists():
        user_train_dir_list = list(user_data_dir.glob(r"*[T|t]rain*"))
        user_test_dir_list = list(user_data_dir.glob(r"*[T|t]est*"))

        if len(list(user_train_dir_list)) == 1:
            user_train_dir = list(user_train_dir_list)[0]
            try:
                user_train_dir.rename(train_dir)
            except Exception as e:
                print("already exists, stop")
            
        else:
            raise Exception("Wrong train dataset!")

        if len(list(user_test_dir_list)) == 1:
            user_test_dir = list(user_test_dir_list)[0]
            try:
                user_test_dir.rename(test_dir)
            except Exception as e:
                print("already exists, stop")
        else:
            raise Exception("Wrong test dataset!")

if __name__ == '__main__':
    main()
