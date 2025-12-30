import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F

class SiameseNet(nn.Module):
    def __init__(self, emb_dim=128):
        super().__init__()
        backbone = models.resnet18(pretrained=True)
        self.feature = nn.Sequential(*list(backbone.children())[:-1])
        self.fc = nn.Linear(512, emb_dim)

    def forward_once(self, x):
        x = self.feature(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return F.normalize(x, dim=1)

    def forward(self, x1, x2):
        return self.forward_once(x1), self.forward_once(x2)
