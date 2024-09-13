from einops import rearrange
import torch.nn as nn
import torchvision
import torch

class BilinearNet(nn.Module):
    def __init__(self, num_classes, net = 'vgg', layer_num=22, train=True, drop=0.5):
        super().__init__()

        if net == 'vgg':
            self.net = torchvision.models.vgg16_bn(weights=torchvision.models.VGG16_BN_Weights.IMAGENET1K_V1)
            self.net = self.net.features[:layer_num]
        if net == 'res':
            self.net = torchvision.models.resnet50(weights=torchvision.models.ResNet50_Weights.IMAGENET1K_V2)
            self.net = nn.Sequential(*list(self.net.children())[:layer_num])

        if net == 'den':
            self.net = torchvision.models.densenet121(torchvision.models.DenseNet121_Weights.DEFAULT)
            self.net = nn.Sequential(*list(self.net.children())[:-1])

        self.drop = drop

        self.feat = int(self.net(torch.rand(1, 3, 250, 250)).shape[1])

        self.out = nn.Linear(in_features=self.feat*self.feat, out_features=num_classes)

        self.set_req_grad(req_grad=False)

    
    def set_req_grad(self, req_grad=False):
        for param in self.net.parameters():
            param.requires_grad = req_grad


    def outter_product(self, x1, x2):
        # change to channels last
        x1 = rearrange(x1, 'b c h w -> b h w c')
        x2 = rearrange(x2, 'b c h w -> b h w c')

        # outter product
        phi_I = torch.einsum('i j k m, i j k n -> i m n',x1, x2)

        phi_I = torch.reshape(phi_I, (-1,x1.shape[-1]*x1.shape[-1]))
        phi_I = torch.div(phi_I,x1.shape[1]*x1.shape[2])

        y_ssqrt = torch.mul(torch.sign(phi_I),torch.sqrt(torch.abs(phi_I)+1e-12))
        z_l2 = torch.nn.functional.normalize(y_ssqrt, p=2)

        return z_l2


    def forward(self, x):
        # get pretrained VGG inner representation
        _x = self.net(x)

        # randomize each representation differently
        x1 = nn.functional.dropout(_x, p=self.drop)
        x2 = nn.functional.dropout(_x, p=self.drop)

        # bilinear operation
        bi_out = self.outter_product(x1, x2)

        out = self.out(bi_out)

        return out
