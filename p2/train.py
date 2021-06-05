import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import numpy as np

from Net import CNN
from flush import standardize_all


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
        all_data.append(fea_av)
        all_data = np.array(all_data)
    # 返回每个人的feature平均，整合在all里
    return all_data


def init_data():
    standardize_all()
    val_dir = 'D:/data/save/photo'
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
    all_data = cal(net=net, data_loader=val_loader, device=device)
    np.savez('D:/data/save/data.npz', data=all_data)
    print("done")