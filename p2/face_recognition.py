import sklearn
from sklearn import metrics
import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import numpy as np

import DataBase
from Net import CNN
from flush import before_recognize


def cal(net, data_loader, device):
    """
    fea_list = []
    with torch.no_grad():
        for data in data_loader:
            images, labels = data[0].to(device), data[1].to(device)
            middle = net.my_feature(images)
            middle = middle.cpu().numpy()
            fea_list.append(middle[0])
        fea_av = np.mean(fea_list, 0)  # 压缩行，返回1*n矩阵
        fea_av = np.array(fea_av)
        fea_av = [fea_av]
    return fea_av
    """
    fea_list = []
    with torch.no_grad():
        for data in data_loader:
            images, labels = data[0].to(device), data[1].to(device)
            middle = net.my_feature(images)
            middle = middle.cpu().numpy()
            tmp = np.array(middle[0])
            tmp = [tmp]
            fea_list.append(tmp)
    return fea_list


def recognize():
    before_recognize()
    val_dir = 'D:/data/capture/out'
    normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

    val_set = datasets.ImageFolder(
        val_dir,
        transforms.Compose([
            transforms.ToTensor(),
            normalize,
        ]))

    val_loader = torch.utils.data.DataLoader(val_set)
    net = CNN()
    state_dict = torch.load('D:/data/save/par.pkl')
    net.load_state_dict(state_dict)

    device = torch.device('cuda')
    net.to(device)

    '''
    fea = cal(net=net, data_loader=val_loader, device=device)
    data = np.load('D:/data/save/data.npz')
    all_data = data['data']
    data.close()
    dist = metrics.pairwise.cosine_similarity(fea, all_data)
    pred = np.argmax(dist, 1)
    print(dist[0])
    print(dist[0][pred], pred)
    if dist[0][pred] > 0.986:
        return pred[0]
    else:
        print("不在库中")
        return 0
    '''

    fea = cal(net=net, data_loader=val_loader, device=device)
    data = np.load('D:/data/save/data.npz')
    all_data = data['data']
    data.close()

    dist0 = metrics.pairwise.cosine_similarity(fea[0], all_data)
    pred0 = np.argmax(dist0, 1)
    dist1 = metrics.pairwise.cosine_similarity(fea[1], all_data)
    pred1 = np.argmax(dist1, 1)

    print(dist0[0])
    print(dist0[0][pred0], pred0)
    print(dist1[0][pred1], pred1)
    if pred0 == pred1 and min(dist0[0][pred0], dist1[0][pred1]) > 0.985:
        return pred0[0]
    else:
        print("不在库中")
        return 0
