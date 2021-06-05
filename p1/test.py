import glob
import os

import cv2
import sklearn
import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import numpy as np

import dao
import fea_check
import file_save
from main import CNN


def cal(net, data_loader, device):
    fea_list = []
    all_data = []
    with torch.no_grad():
        flag = True
        tmp = None
        for data in data_loader:
            images, labels = data[0].to(device), data[1].to(device)
            fea = net.my_feature(images)
            middle = fea.cpu().numpy()
            if flag:  # 首次循环
                flag = False
                tmp = labels
                fea_list.append(middle[0])
            elif tmp != labels:  # 新的标签
                tmp = labels
                fea_av = np.mean(fea_list, 0)  # 压缩行，返回1*n矩阵
                all_data.append(fea_av)
                fea_list.clear()
                fea_list.append(middle[0])
            else:
                fea_list.append(middle[0])
        fea_av = np.mean(fea_list, 0)  # 压缩行，返回1*n矩阵
        fea_av = np.array(fea_av)
        fea_av = [fea_av]
        all_data = np.array(all_data)

    # 返回每个人的feature平均，整合在all里
    return all_data, fea_av


if __name__ == '__main__':
    val_dir = './data/t'
    normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

    val_set = datasets.ImageFolder(
        val_dir,
        transforms.Compose([
            transforms.Resize(100),
            transforms.CenterCrop(100),
            transforms.ToTensor(),
            normalize,
        ]))
    batch_size = 1

    val_loader = torch.utils.data.DataLoader(val_set)
    net = CNN()
    state_dict = torch.load('./par.pkl')
    net.load_state_dict(state_dict)

    device = torch.device('cuda')
    net.to(device)

    all_data, fea = cal(net=net, data_loader=val_loader, device=device)
    # all_data2 = file_save.read()

    print(fea)
    print(all_data)
    dist = sklearn.metrics.pairwise.cosine_similarity(fea, all_data)
    pred = np.argmax(dist, 1)
    print(dist[0])
    print(dist[0][pred], pred)
    if dist[0][pred] > 0.98:
        dao.get_name(pred[0])
    else:
        print("不在库中")
