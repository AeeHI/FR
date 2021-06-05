import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np
import os


class CNN(nn.Module):
    def __init__(self):
        # 注意:首先调用父类的初始化函数
        super(CNN, self).__init__()
        # 定义卷积、池化以及全连接操作
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1)

        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.bn1 = nn.BatchNorm2d(16)
        self.bn2 = nn.BatchNorm2d(32)
        self.bn3 = nn.BatchNorm2d(64)
        self.bn4 = nn.BatchNorm2d(128)

        self.fc1 = nn.Linear(25 * 25 * 128, 1024)  # 600
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(1024, 1024)
        self.fc3 = nn.Linear(1024, 128)

    def forward(self, x):
        x = self.bn1(F.relu(self.conv1(x)))
        x = self.bn2(F.relu(self.conv2(x)))
        x = self.bn3(F.relu(self.conv3(x)))
        x = self.pool(x)
        x = self.bn4(F.relu(self.conv4(x)))
        x = self.pool(x)
        #         x = self.poo15(F.relu(self.conv5(x)))
        # 使用torch.Tensor.view函数，把一个多维张量拉直为一个1维张量(向量)

        x = x.view(x.size(0), -1)
        # 全连接层
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        x = F.log_softmax(x, dim=1)
        return x

    def my_feature(self, x):
        x = self.bn1(F.relu(self.conv1(x)))
        x = self.bn2(F.relu(self.conv2(x)))
        x = self.bn3(F.relu(self.conv3(x)))
        x = self.pool(x)
        x = self.bn4(F.relu(self.conv4(x)))
        x = self.pool(x)
        #         x = self.poo15(F.relu(self.conv5(x)))
        # 使用torch.Tensor.view函数，把一个多维张量拉直为一个1维张量(向量)

        x = x.view(x.size(0), -1)
        # 全连接层
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


losslist = []


def train(net, optimizer, loss_fn, num_epoch, data_loader, device):
    net.train()  # 进入训练模式
    for epoch in range(num_epoch):
        running_loss = 0.0
        for i, data in enumerate(data_loader):
            inputs, labels = data[0].to(device), data[1].to(device)
            optimizer.zero_grad()
            outputs = net(inputs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            # print('%d batch:%f'%(i+1,loss.item()))
        print('%d epoch:%f' % (epoch + 1, running_loss / batch_size))
        losslist.append(running_loss / batch_size)


def evaluate(net, data_loader, device):
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
    C = confusion_matrix(true_list, predicted_list)

    return acc, C


def show_confMat(confusion_mat, classes_name, set_name, out_dir):
    """
    可视化混淆矩阵，保存png格式
    :param confusion_mat: nd-array
    :param classes_name: list,各类别名称
    :param set_name: str, eg: 'valid', 'train'
    :param out_dir: str, png输出的文件夹
    :return:
    """
    # 归一化
    confusion_mat_N = confusion_mat.copy()
    for i in range(len(classes_name)):
        confusion_mat_N[i, :] = confusion_mat[i, :] / confusion_mat[i, :].sum()

    # 获取颜色
    cmap = plt.cm.get_cmap('Greys')  # 更多颜色: http://matplotlib.org/examples/color/colormaps_reference.html
    plt.imshow(confusion_mat_N, cmap=cmap)
    #     plt.colorbar()

    # 设置文字
    xlocations = np.array(range(len(classes_name)))
    plt.xticks(xlocations, classes_name, rotation=60)
    plt.yticks(xlocations, classes_name)
    plt.xlabel('Predict label')
    plt.ylabel('True label')
    plt.title('Confusion_Matrix_' + set_name)

    # 打印数字
    for i in range(confusion_mat_N.shape[0]):
        for j in range(confusion_mat_N.shape[1]):
            plt.text(x=j, y=i, s=int(confusion_mat[i, j]), va='center', ha='center', color='red', fontsize=10)
    # 保存
    plt.savefig(os.path.join(out_dir, 'Confusion_Matrix_' + set_name + '.png'))
    plt.close()


if __name__ == '__main__':
    # 数据集
    train_dir = 'D:/a/a'
    val_dir = 'D:/a/b'
    normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    train_set = datasets.ImageFolder(
        train_dir,
        transforms.Compose([
            # transforms.Resize(101),
            # transforms.CenterCrop(100),
            # transforms.RandomResizedCrop(100),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            normalize,
        ]))
    val_set = datasets.ImageFolder(
        val_dir,
        transforms.Compose([
            # transforms.Resize(100),
            # transforms.CenterCrop(100),
            transforms.ToTensor(),
            normalize,
        ]))
    batch_size = 1
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size,
                                               shuffle=True, num_workers=2)
    val_loader = torch.utils.data.DataLoader(val_set, batch_size=batch_size,
                                             shuffle=False, num_workers=2)
    # 参数初始化
    net = CNN()
    state_dict = torch.load('./par.pkl')
    net.load_state_dict(state_dict=state_dict)

    device = torch.device('cuda')
    net.to(device)
    xentropy = nn.CrossEntropyLoss()

    optimizer = optim.Adam(net.parameters(), lr=0.000001)

    num_epoch = 1
    # 训练和评估
    train(net=net,
          optimizer=optimizer,
          loss_fn=xentropy,
          num_epoch=num_epoch,
          data_loader=train_loader,
          device=device)
    train_acc, C1 = evaluate(net=net,
                             data_loader=train_loader,
                             device=device)
    val_acc, C2 = evaluate(net=net,
                           data_loader=val_loader,
                           device=device)

    asd = [i for i in range(59)]

    '''
    show_confMat(C1, asd, "a", "D:/a/")
    show_confMat(C2, asd, "b", "D:/a/")
    # torch.save(net.state_dict(), 'D:/' + datetime.datetime.now().strftime("%Y%m%d%H%M") + '.pth')'''
    print('Training Accuracy: %.2f%%' % (100 * train_acc))
    print('Val Accuracy: %.2f%%' % (100 * val_acc))
    torch.save(net.state_dict(), './par2.pkl')

    # 画损失函数图
    print(losslist)
    plt.plot(losslist[1:])
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.title('')
    plt.savefig(os.path.join('D:/0.png'))
    plt.close()
