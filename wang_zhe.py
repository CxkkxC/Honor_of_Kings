#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/28 8:40
# @Author  : Cxk
# @File    : wang_zhe.py

# class6_陈旋凯_511721010639_王者荣耀英雄信息获取

import requests
import lxml.html
import os
import re


def parse_wangzhe_url(html_url):
    """
    爬取整个网页内容
    :param html_url:
    :return:
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    response = requests.get(html_url, headers=headers)
    response.encoding = 'gbk'
    html_content = response.text
    return html_content


def get_hero_data(html_datas):
    """
    提取英雄信息保存为csv文件时使用的函数
    :param html_datas:
    :return:
    """
    metree = lxml.html.etree

    parser = metree.HTML(html_datas)

    hero_list = parser.xpath("//div[@class='herolist-content']/ul[@class='herolist clearfix']/li")

    # print(len(hero_list))
    lists = []
    for i in hero_list:
        hero_item = []
        hero_name = i.xpath("./a/text()")[0]
        hero_item.append(hero_name)
        # print(hero_name)
        hero_img = "http:" + i.xpath("./a/img/@src")[0]
        hero_item.append(hero_img)
        # print(hero_img)
        hero_info = "https://pvp.qq.com/web201605/" + i.xpath("./a/@href")[0]
        hero_item.append(hero_info)
        # print(hero_info)
        lists.append(hero_item)
    return lists


def get_hero_data2(html_datas):
    """
    提取英雄信息保存图片时使用的函数
    :param html_datas:
    :return:
    """
    metree = lxml.html.etree

    parser = metree.HTML(html_datas)

    hero_list = parser.xpath("//div[@class='herolist-content']/ul[@class='herolist clearfix']/li")

    # print(len(hero_list))
    lists = []
    for i in hero_list:
        hero_name = i.xpath("./a/text()")[0]
        lists.append(hero_name)
        # print(hero_name)
        hero_img = "http:" + i.xpath("./a/img/@src")[0]
        lists.append(hero_img)
        # print(hero_img)
        hero_info = "https://pvp.qq.com/web201605/" + i.xpath("./a/@href")[0]
        lists.append(hero_info)
        # print(hero_info)
    return lists


def save_img(hero_datas):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    # print(len(hero_datas))
    dir_name = "./hero_img/"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    for j in range(0, 279, 3):
        # print(hero_datas[j+1])
        response = requests.get(hero_datas[j + 1], headers=headers)
        image_content = response.content
        paths = dir_name + hero_datas[j] + ".jpg"
        writer = open(paths, "wb")
        writer.write(image_content)
        writer.close()
    print("英雄头像下载完成!")


def save_hero_datas(hero_datas):
    """
    保存为csv文件
    :param hero_datas:
    :return:
    """
    dir_name = "./herofile"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    hero_file = open(dir_name + "./hero.csv", "w", encoding="gbk")
    hero_file.write("name,imgUrl,infoUrl\n")
    # print(hero_datas)
    for element in hero_datas:
        # print(element)
        hero = ','.join(element)
        # print(hero)
        hero_file.write(hero + "\n")
    hero_file.close()
    print("英雄信息保存为csv文件完成!")


def get_hero_info_url(hero_datas):
    """
    获取英雄详细信息地址,返回地址列表
    :param hero_datas:
    :return:
    """
    list2 = []
    for j in range(0, 279, 3):
        list2.append(hero_datas[j])
        list2.append(hero_datas[j + 2])
    return list2


def save_hero_pifu(hero_info_url):
    """
    获取英雄皮肤并保存
    :param hero_info_url:
    :return:
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    list3 = []
    j = 0
    dir_name = "./hero_pifu/"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    for k in range(0, 186,2):
        # print(hero_info_url[k+1])
        response = requests.get(hero_info_url[k + 1], headers=headers)
        response.encoding = 'gbk'
        html_content = response.text
        metree = lxml.html.etree

        parser = metree.HTML(html_content)

        hero_pifu = str(parser.xpath("//div[@class='zk-con1 zk-con']/@style")[0])
        # print(hero_pifu)

        # 正则表达式去除单引号
        m = re.compile("'.*'")
        # eval()函数去除字符串两边引号
        url = eval(m.findall(hero_pifu)[0])
        for l in ['1', '2', '3', '4', '5', '6', '7']:
            url = list(url)
            url[-5] = l
            url = ''.join(url)
            # 合成皮肤地址
            pifu_url = "http:" + url
            response = requests.get(pifu_url, headers=headers)
            # 获取皮肤图片并下载
            if response:
                image_content = response.content
                # 图片保存路径
                paths = dir_name + hero_info_url[k] + str(j) + ".jpg"
                # 打开并写入图片
                writer = open(paths, "wb")
                writer.write(image_content)
                writer.close()
                j += 1
            else:
                j=0
                break
    print("皮肤下载完成!")
    """
    实验
    """
    # k = "https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/180/180-bigskin-1.jpg"
    # response = requests.get(k, headers=headers)
    # if response:
    #     print('有图片')
    # else:
    #     print("无图")
    # print(type(response))
    # response.encoding = 'gbk'
    # html_content = response.text
    # # print(html_content)
    # metree = lxml.html.etree
    #
    # parser = metree.HTML(html_content)
    #
    # hero_pifu = parser.xpath("//div[@class='zk-con1 zk-con']/@style")
    # print(hero_pifu)


def main():
    """
    主函数
    :return:
    """
    html_url = "https://pvp.qq.com/web201605/herolist.shtml"

    html_datas = parse_wangzhe_url(html_url)

    #     保存为csv文件时提取数据
    hero_datas = get_hero_data(html_datas)

    #     保存英雄图片文件时提取数据
    hero_datas2 = get_hero_data2(html_datas)

    # 保存英雄图片
    save_img(hero_datas2)

    # 保存英雄信息
    save_hero_datas(hero_datas)

    # 获取英雄信息地址
    hero_info_url = get_hero_info_url(hero_datas2)
    # print(len(get_hero_info_url(hero_datas2)))186
    #  传入地址并下载保存皮肤
    save_hero_pifu(hero_info_url)


if __name__ == '__main__':
    main()
