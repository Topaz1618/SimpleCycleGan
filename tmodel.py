import argparse
import sys
import os
import matplotlib.pyplot as plt
import imageio


import torchvision.transforms as transforms
from torchvision.utils import save_image
from torch.utils.data import DataLoader
from torch.autograd import Variable
import torch

import util
import network

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))
sys.path.append(BASE_DIR)

class Myoption():
    def __init__(self):
        # self.dataset = "horse2zebra"
        self.dataset = "mnist"
        self.train_subfolder = "train"
        self.test_subfolder = "test"
        self.input_ngc = 3
        self.output_ngc = 3
        self.input_ndc = 3
        self.output_ndc = 1
        self.batch_size = 32
        self.ngf = 32
        self.ndf = 64
        self.nb = 9
        # hz
        # self.input_size = 256
        # self.resize_scale = 286
        # self.train_epoch = 200
        # self.decay_epoch = 100

        # mnist
        self.input_size = 28
        self.resize_scale = 32
        self.train_epoch = 200
        self.decay_epoch = 120

        self.crop = True
        self.fliplr = True
        self.lrD = 0.0002
        self.lrG = 0.0002
        self.lambdaA = 10
        self.lambdaB = 10
        self.beta1 = 0.5
        self.beta2 = 0.999
        self.save_root = "results"
        self.output_path = "output"


opt = Myoption()


###### Definition of variables ######
# Networks
netG_A2B = network.generator(opt.input_ngc, opt.output_ngc, opt.ngf, opt.nb)
netG_B2A = network.generator(opt.input_ngc, opt.output_ngc, opt.ngf, opt.nb)


netG_A2B.cuda()
netG_B2A.cuda()

# Load state dicts

netG_A2B.load_state_dict(torch.load('/mnt/mnist_results/mnist_generatorA_param.pkl'))
# netG_B2A.load_state_dict(torch.load('/mnt/mnist_results/mnist_generatorB_param.pkl'))

# Set model's test mode
netG_A2B.eval()
# netG_B2A.eval()

transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
])

dataset_path = "/mnt/data/mnist"
test_loader_A = util.data_load(dataset_path, f"{opt.test_subfolder}A", transform, opt.batch_size, shuffle=False)

idx = 0
for realA, _ in test_loader_A:
    print("A", type(realA), realA.shape)
    realA = Variable(realA.cuda(), volatile=True)
    genB = netG_A2B(realA)
    print("B", type(realA), realA.shape)

    path = os.path.join('/mnt/mnist_results/final_res', f"{str(idx)}_output.png")
    plt.imsave(path, (genB[0].cpu().data.numpy().transpose(1, 2, 0) + 1) / 2)
    idx += 1
