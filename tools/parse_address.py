# -*- coding: utf-8 -*-
import codecs
import jieba

addr_list = ["四川省成都市龙泉驿区","四川省攀枝花市", "四川省攀枝花市米易县", "广西壮族自治区南宁市良庆区","重庆市沙坪坝区"]


def segment():
    for addr in addr_list:
        seg_list = jieba.cut(addr, cut_all=False)
        print(", ".join(seg_list))


if __name__ == "__main__":
    segment()
