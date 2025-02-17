import os

import torch
from torch.utils.data import DataLoader
import torchvision

from .basic_dataset import FedDataset, BaseDataset



class SyntheticDataset(FedDataset):
    def __init__(self, root, path, preprocess=False) -> None:

        if preprocess is True:
            self.preprocess(root, path)
        else:
            print("Warning: please make sure that you have preprocess the data once!")

    def preprocess(self, root, path, partition=0.2):

        if os.path.exists(self.path) is not True:
            os.mkdir(self.path)
            os.mkdir(os.path.join(self.path, "train"))
            os.mkdir(os.path.join(self.path, "var"))
            os.mkdir(os.path.join(self.path, "test"))

        raw_data = torch.load(root)
        users, user_data = raw_data["users"], raw_data["user_data"]

        for id in users:
            data, label = user_data[id]['x'], user_data[id]['y']
            train_size = int(len(label)*partition)

            trainset = BaseDataset(data[0:train_size], label[0:train_size])
            torch.save(os.path.join(path, "train","data{}.pkl".format(id)), trainset)

            testset = BaseDataset(data[train_size:], label[train_size:])
            torch.save(os.path.join(path, "test","data{}.pkl".format(id)), testset)

    def get_dataset(self, id, type="train"):
        dataset = torch.load(
            os.path.join(self.path, type, "data{}.pkl".format(id)))
        return dataset

    def get_dataloader(self, id, batch_size, type="train"):
        dataset = self.get_dataset(id, type)
        batch_size = len(dataset) if batch_size is None else batch_size
        data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        return data_loader