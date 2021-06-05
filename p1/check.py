import glob
import os

import cv2
import sklearn
import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import numpy as np
from main import CNN


def cal(net, data_loader, device):
    net.eval()  # 进入模型评估模式
    correct = 0
    total = 0
    predicted_list = []
    true_list = []
    with torch.no_grad():
        for data in data_loader:
            images, labels = data[0].to(device), data[1].to(device)
            true_list = np.append(true_list, labels.cpu().numpy())
            outputs = net(images)
            predicted = torch.argmax(outputs.data, 1)
            predicted_list = np.append(predicted_list, predicted.cpu().numpy())
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    acc = correct / total
    return acc

'''
def load_db(db_path, label, db):
    if not os.path.exists(db_path):
        print('Database path is not existed!')
    folders = sorted(glob.glob(os.path.join(db_path, '*')))
    for name in folders:

        print('loading {}:'.format(name))
        label.append(os.path.basename(name))
        img_list = glob.glob(os.path.join(name, '*.jpg'))

        imgs = [cv2.imread(img) for img in img_list]

        fea = net.my_feature(imgs)

        # print('fea.shape {}'.format(fea.shape))
        fea = np.mean(fea, 0)  # 压缩行，返回1*n矩阵
        print(fea[:])
        if db is None:
            db = fea.copy()
        else:
            db = np.vstack((db, fea.copy()))

        # print fea
        print('done')
    print(label)
'''

if __name__ == '__main__':
    val_dir = 'D:/a/b'
    normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

    val_set = datasets.ImageFolder(
        val_dir,
        transforms.Compose([
            transforms.ToTensor(),
            normalize,
        ]))
    batch_size = 32

    val_loader = torch.utils.data.DataLoader(val_set, batch_size=batch_size,
                                             shuffle=False, num_workers=2)
    net = CNN()
    state_dict = torch.load('./par.pkl')
    net.load_state_dict(state_dict)

    device = torch.device('cuda')
    net.to(device)

    val_acc = cal(net=net, data_loader=val_loader, device=device)
    print(val_acc)
