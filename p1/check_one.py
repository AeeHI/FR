import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import numpy as np

from main import CNN


def cal(net, data_loader, device):
    fea_list = []
    with torch.no_grad():
        for data in data_loader:
            images = data[0].to(device)
            fea = net.my_feature(images)
            middle = fea.cpu().numpy()
            fea_list.append(middle[0])
        fea_av = np.mean(fea_list, 0)  # 压缩行，返回1*n矩阵
        fea_av = np.array(fea_av)
        fea_av = [fea_av]
    return fea_av


if __name__ == '__main__':
    val_dir = "D:\data\capture"
    normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

    val_set = datasets.ImageFolder(
        val_dir,
        transforms.Compose([
            transforms.Resize(110),
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

    all_data = cal(net=net, data_loader=val_loader, device=device)

    print(all_data)
