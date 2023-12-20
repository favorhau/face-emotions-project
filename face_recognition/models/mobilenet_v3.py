# from typing import Callable, List, Optional

# import torch
# from torch import nn, Tensor
# from torch.nn import functional as F
# from functools import partial


# def _make_divisible(ch, divisor=8, min_ch=None):
#     """
#     This function is taken from the original tf repo.
#     It ensures that all layers have a channel number that is divisible by 8
#     It can be seen here:
#     https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet/mobilenet.py
#     """
#     if min_ch is None:
#         min_ch = divisor
#     new_ch = max(min_ch, int(ch + divisor / 2) // divisor * divisor)
#     # Make sure that round down does not go down by more than 10%.
#     if new_ch < 0.9 * ch:
#         new_ch += divisor
#     return new_ch


# class ConvBNActivation(nn.Sequential):
#     def __init__(self,
#                  in_planes: int,
#                  out_planes: int,
#                  kernel_size: int = 3,
#                  stride: int = 1,
#                  groups: int = 1,
#                  norm_layer: Optional[Callable[..., nn.Module]] = None,
#                  activation_layer: Optional[Callable[..., nn.Module]] = None):
#         padding = (kernel_size - 1) // 2
#         if norm_layer is None:
#             norm_layer = nn.BatchNorm2d
#         if activation_layer is None:
#             activation_layer = nn.ReLU6
#         super(ConvBNActivation, self).__init__(nn.Conv2d(in_channels=in_planes,
#                                                          out_channels=out_planes,
#                                                          kernel_size=kernel_size,
#                                                          stride=stride,
#                                                          padding=padding,
#                                                          groups=groups,
#                                                          bias=False),
#                                                norm_layer(out_planes),
#                                                activation_layer(inplace=True))


# class SqueezeExcitation(nn.Module):
#     def __init__(self, input_c: int, squeeze_factor: int = 4):
#         super(SqueezeExcitation, self).__init__()
#         squeeze_c = _make_divisible(input_c // squeeze_factor, 8)
#         self.fc1 = nn.Conv2d(input_c, squeeze_c, 1)
#         self.fc2 = nn.Conv2d(squeeze_c, input_c, 1)

#     def forward(self, x: Tensor) -> Tensor:
#         scale = F.adaptive_avg_pool2d(x, output_size=(1, 1))
#         scale = self.fc1(scale)
#         scale = F.relu(scale, inplace=True)
#         scale = self.fc2(scale)
#         scale = F.hardsigmoid(scale, inplace=True)
#         return scale * x


# class InvertedResidualConfig:
#     def __init__(self,
#                  input_c: int,
#                  kernel: int,
#                  expanded_c: int,
#                  out_c: int,
#                  use_se: bool,
#                  activation: str,
#                  stride: int,
#                  width_multi: float):
#         self.input_c = self.adjust_channels(input_c, width_multi)
#         self.kernel = kernel
#         self.expanded_c = self.adjust_channels(expanded_c, width_multi)
#         self.out_c = self.adjust_channels(out_c, width_multi)
#         self.use_se = use_se
#         self.use_hs = activation == "HS"  # whether using h-swish activation
#         self.stride = stride

#     @staticmethod
#     def adjust_channels(channels: int, width_multi: float):
#         return _make_divisible(channels * width_multi, 8)


# class InvertedResidual(nn.Module):
#     def __init__(self,
#                  cnf: InvertedResidualConfig,
#                  norm_layer: Callable[..., nn.Module]):
#         super(InvertedResidual, self).__init__()

#         if cnf.stride not in [1, 2]:
#             raise ValueError("illegal stride value.")

#         self.use_res_connect = (cnf.stride == 1 and cnf.input_c == cnf.out_c)

#         layers: List[nn.Module] = []
#         activation_layer = nn.Hardswish if cnf.use_hs else nn.ReLU

#         # expand
#         if cnf.expanded_c != cnf.input_c:
#             layers.append(ConvBNActivation(cnf.input_c,
#                                            cnf.expanded_c,
#                                            kernel_size=1,
#                                            norm_layer=norm_layer,
#                                            activation_layer=activation_layer))

#         # depthwise
#         layers.append(ConvBNActivation(cnf.expanded_c,
#                                        cnf.expanded_c,
#                                        kernel_size=cnf.kernel,
#                                        stride=cnf.stride,
#                                        groups=cnf.expanded_c,
#                                        norm_layer=norm_layer,
#                                        activation_layer=activation_layer))

#         if cnf.use_se:
#             layers.append(SqueezeExcitation(cnf.expanded_c))

#         # project
#         layers.append(ConvBNActivation(cnf.expanded_c,
#                                        cnf.out_c,
#                                        kernel_size=1,
#                                        norm_layer=norm_layer,
#                                        activation_layer=nn.Identity))

#         self.block = nn.Sequential(*layers)
#         self.out_channels = cnf.out_c
#         self.is_strided = cnf.stride > 1

#     def forward(self, x: Tensor) -> Tensor:
#         result = self.block(x)
#         if self.use_res_connect:
#             result += x

#         return result


# class MobileNetV3(nn.Module):
#     def __init__(self,
#                  inverted_residual_setting: List[InvertedResidualConfig],
#                  last_channel: int,
#                  num_classes: int = 1000,
#                  block: Optional[Callable[..., nn.Module]] = None,
#                  norm_layer: Optional[Callable[..., nn.Module]] = None):
#         super(MobileNetV3, self).__init__()

#         if not inverted_residual_setting:
#             raise ValueError("The inverted_residual_setting should not be empty.")
#         elif not (isinstance(inverted_residual_setting, List) and
#                   all([isinstance(s, InvertedResidualConfig) for s in inverted_residual_setting])):
#             raise TypeError("The inverted_residual_setting should be List[InvertedResidualConfig]")

#         if block is None:
#             block = InvertedResidual

#         if norm_layer is None:
#             norm_layer = partial(nn.BatchNorm2d, eps=0.001, momentum=0.01)

#         layers: List[nn.Module] = []

#         # building first layer
#         firstconv_output_c = inverted_residual_setting[0].input_c
#         layers.append(ConvBNActivation(3,
#                                        firstconv_output_c,
#                                        kernel_size=3,
#                                        stride=2,
#                                        norm_layer=norm_layer,
#                                        activation_layer=nn.Hardswish))
#         # building inverted residual blocks
#         for cnf in inverted_residual_setting:
#             layers.append(block(cnf, norm_layer))

#         # building last several layers
#         lastconv_input_c = inverted_residual_setting[-1].out_c
#         lastconv_output_c = 6 * lastconv_input_c
#         layers.append(ConvBNActivation(lastconv_input_c,
#                                        lastconv_output_c,
#                                        kernel_size=1,
#                                        norm_layer=norm_layer,
#                                        activation_layer=nn.Hardswish))
#         self.features = nn.Sequential(*layers)
#         self.avgpool = nn.AdaptiveAvgPool2d(1)
#         self.classifier = nn.Sequential(nn.Linear(lastconv_output_c, last_channel),
#                                         nn.Hardswish(inplace=True),
#                                         nn.Dropout(p=0.5, inplace=True),
#                                         nn.Linear(last_channel, num_classes))

#         # initial weights
#         for m in self.modules():
#             if isinstance(m, nn.Conv2d):
#                 nn.init.kaiming_normal_(m.weight, mode="fan_out")
#                 if m.bias is not None:
#                     nn.init.zeros_(m.bias)
#             elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
#                 nn.init.ones_(m.weight)
#                 nn.init.zeros_(m.bias)
#             elif isinstance(m, nn.Linear):
#                 nn.init.normal_(m.weight, 0, 0.01)
#                 nn.init.zeros_(m.bias)

#     def _forward_impl(self, x: Tensor) -> Tensor:
#         x = self.features(x)
#         x = self.avgpool(x)
#         x = torch.flatten(x, 1)
#         x = self.classifier(x)

#         return x

#     def forward(self, x: Tensor) -> Tensor:
#         return self._forward_impl(x)


# def mobilenet_v3_large(num_classes: int = 1000,
#                        reduced_tail: bool = False) -> MobileNetV3:
#     """
#     Constructs a large MobileNetV3 architecture from
#     "Searching for MobileNetV3" <https://arxiv.org/abs/1905.02244>.

#     weights_link:
#     https://download.pytorch.org/models/mobilenet_v3_large-8738ca79.pth

#     Args:
#         num_classes (int): number of classes
#         reduced_tail (bool): If True, reduces the channel counts of all feature layers
#             between C4 and C5 by 2. It is used to reduce the channel redundancy in the
#             backbone for Detection and Segmentation.
#     """
#     width_multi = 1.0
#     bneck_conf = partial(InvertedResidualConfig, width_multi=width_multi)
#     adjust_channels = partial(InvertedResidualConfig.adjust_channels, width_multi=width_multi)

#     reduce_divider = 2 if reduced_tail else 1

#     inverted_residual_setting = [
#         # input_c, kernel, expanded_c, out_c, use_se, activation, stride
#         bneck_conf(16, 3, 16, 16, False, "RE", 1),
#         bneck_conf(16, 3, 64, 24, False, "RE", 2),  # C1
#         bneck_conf(24, 3, 72, 24, False, "RE", 1),
#         bneck_conf(24, 5, 72, 40, True, "RE", 2),  # C2
#         bneck_conf(40, 5, 120, 40, True, "RE", 1),
#         bneck_conf(40, 5, 120, 40, True, "RE", 1),
#         bneck_conf(40, 3, 240, 80, False, "HS", 2),  # C3
#         bneck_conf(80, 3, 200, 80, False, "HS", 1),
#         bneck_conf(80, 3, 184, 80, False, "HS", 1),
#         bneck_conf(80, 3, 184, 80, False, "HS", 1),
#         bneck_conf(80, 3, 480, 112, True, "HS", 1),
#         bneck_conf(112, 3, 672, 112, True, "HS", 1),
#         bneck_conf(112, 5, 672, 160 // reduce_divider, True, "HS", 2),  # C4
#         bneck_conf(160 // reduce_divider, 5, 960 // reduce_divider, 160 // reduce_divider, True, "HS", 1),
#         bneck_conf(160 // reduce_divider, 5, 960 // reduce_divider, 160 // reduce_divider, True, "HS", 1),
#     ]
#     last_channel = adjust_channels(1280 // reduce_divider)  # C5

#     return MobileNetV3(inverted_residual_setting=inverted_residual_setting,
#                        last_channel=last_channel,
#                        num_classes=num_classes)


# def mobilenet_v3_small(num_classes: int = 1000,
#                        reduced_tail: bool = False) -> MobileNetV3:
#     """
#     Constructs a large MobileNetV3 architecture from
#     "Searching for MobileNetV3" <https://arxiv.org/abs/1905.02244>.

#     weights_link:
#     https://download.pytorch.org/models/mobilenet_v3_small-047dcff4.pth

#     Args:
#         num_classes (int): number of classes
#         reduced_tail (bool): If True, reduces the channel counts of all feature layers
#             between C4 and C5 by 2. It is used to reduce the channel redundancy in the
#             backbone for Detection and Segmentation.
#     """
#     width_multi = 1.0
#     bneck_conf = partial(InvertedResidualConfig, width_multi=width_multi)
#     adjust_channels = partial(InvertedResidualConfig.adjust_channels, width_multi=width_multi)

#     reduce_divider = 2 if reduced_tail else 1

#     inverted_residual_setting = [
#         # input_c, kernel, expanded_c, out_c, use_se, activation, stride
#         bneck_conf(16, 3, 16, 16, True, "RE", 2),  # C1
#         bneck_conf(16, 3, 72, 24, False, "RE", 2),  # C2
#         bneck_conf(24, 3, 88, 24, False, "RE", 1),
#         bneck_conf(24, 5, 96, 40, True, "HS", 2),  # C3
#         bneck_conf(40, 5, 240, 40, True, "HS", 1),
#         bneck_conf(40, 5, 240, 40, True, "HS", 1),
#         bneck_conf(40, 5, 120, 48, True, "HS", 1),
#         bneck_conf(48, 5, 144, 48, True, "HS", 1),
#         bneck_conf(48, 5, 288, 96 // reduce_divider, True, "HS", 2),  # C4
#         bneck_conf(96 // reduce_divider, 5, 576 // reduce_divider, 96 // reduce_divider, True, "HS", 1),
#         bneck_conf(96 // reduce_divider, 5, 576 // reduce_divider, 96 // reduce_divider, True, "HS", 1)
#     ]
#     last_channel = adjust_channels(1024 // reduce_divider)  # C5

#     return MobileNetV3(inverted_residual_setting=inverted_residual_setting,
#                        last_channel=last_channel,
#                        num_classes=num_classes)


'''MobileNetV3 in PyTorch.

See the paper "Inverted Residuals and Linear Bottlenecks:
Mobile Networks for Classification, Detection and Segmentation" for more details.
'''
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init



class hswish(nn.Module):
    def forward(self, x):
        out = x * F.relu6(x + 3, inplace=True) / 6
        return out


class hsigmoid(nn.Module):
    def forward(self, x):
        out = F.relu6(x + 3, inplace=True) / 6
        return out


class SeModule(nn.Module):
    def __init__(self, in_size, reduction=4):
        super(SeModule, self).__init__()
        expand_size =  max(in_size // reduction, 8)
        self.se = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(in_size, expand_size, kernel_size=1, bias=False),
            nn.BatchNorm2d(expand_size),
            nn.ReLU(inplace=True),
            nn.Conv2d(expand_size, in_size, kernel_size=1, bias=False),
            nn.Hardsigmoid()
        )

    def forward(self, x):
        return x * self.se(x)


class Block(nn.Module):
    '''expand + depthwise + pointwise'''
    def __init__(self, kernel_size, in_size, expand_size, out_size, act, se, stride):
        super(Block, self).__init__()
        self.stride = stride

        self.conv1 = nn.Conv2d(in_size, expand_size, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(expand_size)
        self.act1 = act(inplace=True)

        self.conv2 = nn.Conv2d(expand_size, expand_size, kernel_size=kernel_size, stride=stride, padding=kernel_size//2, groups=expand_size, bias=False)
        self.bn2 = nn.BatchNorm2d(expand_size)
        self.act2 = act(inplace=True)
        self.se = SeModule(expand_size) if se else nn.Identity()

        self.conv3 = nn.Conv2d(expand_size, out_size, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_size)
        self.act3 = act(inplace=True)

        self.skip = None
        if stride == 1 and in_size != out_size:
            self.skip = nn.Sequential(
                nn.Conv2d(in_size, out_size, kernel_size=1, bias=False),
                nn.BatchNorm2d(out_size)
            )

        if stride == 2 and in_size != out_size:
            self.skip = nn.Sequential(
                nn.Conv2d(in_channels=in_size, out_channels=in_size, kernel_size=3, groups=in_size, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(in_size),
                nn.Conv2d(in_size, out_size, kernel_size=1, bias=True),
                nn.BatchNorm2d(out_size)
            )

        if stride == 2 and in_size == out_size:
            self.skip = nn.Sequential(
                nn.Conv2d(in_channels=in_size, out_channels=out_size, kernel_size=3, groups=in_size, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(out_size)
            )

    def forward(self, x):
        skip = x

        out = self.act1(self.bn1(self.conv1(x)))
        out = self.act2(self.bn2(self.conv2(out)))
        out = self.se(out)
        out = self.bn3(self.conv3(out))
        
        if self.skip is not None:
            skip = self.skip(skip)
        return self.act3(out + skip)



class MobileNetV3_Small(nn.Module):
    def __init__(self, num_classes=1000, act=nn.Hardswish):
        super(MobileNetV3_Small, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=2, padding=1, bias=False)   # note the channel number
        self.bn1 = nn.BatchNorm2d(16)
        self.hs1 = act(inplace=True)

        self.bneck = nn.Sequential(
            Block(3, 16, 16, 16, nn.ReLU, True, 2),
            Block(3, 16, 72, 24, nn.ReLU, False, 2),
            Block(3, 24, 88, 24, nn.ReLU, False, 1),
            Block(5, 24, 96, 40, act, True, 2),
            Block(5, 40, 240, 40, act, True, 1),
            Block(5, 40, 240, 40, act, True, 1),
            Block(5, 40, 120, 48, act, True, 1),
            Block(5, 48, 144, 48, act, True, 1),
            Block(5, 48, 288, 96, act, True, 2),
            Block(5, 96, 576, 96, act, True, 1),
            Block(5, 96, 576, 96, act, True, 1),
        )


        self.conv2 = nn.Conv2d(96, 576, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn2 = nn.BatchNorm2d(576)
        self.hs2 = act(inplace=True)
        self.gap = nn.AdaptiveAvgPool2d(1)

        self.linear3 = nn.Linear(576, 1280, bias=False)
        self.bn3 = nn.BatchNorm1d(1280)
        self.hs3 = act(inplace=True)
        self.drop = nn.Dropout(0.2)
        self.linear4 = nn.Linear(1280, num_classes)
        self.init_params()

    def init_params(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                init.kaiming_normal_(m.weight, mode='fan_out')
                if m.bias is not None:
                    init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                init.constant_(m.weight, 1)
                init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                init.normal_(m.weight, std=0.001)
                if m.bias is not None:
                    init.constant_(m.bias, 0)

    def forward(self, x):
        out = self.hs1(self.bn1(self.conv1(x)))
        out = self.bneck(out)

        out = self.hs2(self.bn2(self.conv2(out)))
        out = self.gap(out).flatten(1)
        out = self.drop(self.hs3(self.bn3(self.linear3(out))))

        return self.linear4(out)


class MobileNetV3_Large(nn.Module):
    def __init__(self, num_classes=1000, act=nn.Hardswish):
        super(MobileNetV3_Large, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=2, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(16)
        self.hs1 = act(inplace=True)

        self.bneck = nn.Sequential(
            Block(3, 16, 16, 16, nn.ReLU, False, 1),
            Block(3, 16, 64, 24, nn.ReLU, False, 2),
            Block(3, 24, 72, 24, nn.ReLU, False, 1),
            Block(5, 24, 72, 40, nn.ReLU, True, 2),
            Block(5, 40, 120, 40, nn.ReLU, True, 1),
            Block(5, 40, 120, 40, nn.ReLU, True, 1),
            Block(3, 40, 240, 80, act, False, 2),
            Block(3, 80, 200, 80, act, False, 1),
            Block(3, 80, 184, 80, act, False, 1),
            Block(3, 80, 184, 80, act, False, 1),
            Block(3, 80, 480, 112, act, True, 1),
            Block(3, 112, 672, 112, act, True, 1),
            Block(5, 112, 672, 160, act, True, 2),
            Block(5, 160, 672, 160, act, True, 1),
            Block(5, 160, 960, 160, act, True, 1),
        )


        self.conv2 = nn.Conv2d(160, 960, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn2 = nn.BatchNorm2d(960)
        self.hs2 = act(inplace=True)
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        self.linear3 = nn.Linear(960, 1280, bias=False)
        self.bn3 = nn.BatchNorm1d(1280)
        self.hs3 = act(inplace=True)
        self.drop = nn.Dropout(0.2)

        self.linear4 = nn.Linear(1280, num_classes)
        self.init_params()

    def init_params(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                init.kaiming_normal_(m.weight, mode='fan_out')
                if m.bias is not None:
                    init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                init.constant_(m.weight, 1)
                init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                init.normal_(m.weight, std=0.001)
                if m.bias is not None:
                    init.constant_(m.bias, 0)

    def forward(self, x):
        out = self.hs1(self.bn1(self.conv1(x)))
        out = self.bneck(out)

        out = self.hs2(self.bn2(self.conv2(out)))
        out = self.gap(out).flatten(1)
        out = self.drop(self.hs3(self.bn3(self.linear3(out))))
        
        return self.linear4(out)