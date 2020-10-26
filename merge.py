#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import yaml
import glob
import argparse
from configer import *

DEFAULT_ATTR = [
    'contexts',
    'clusters',
    'users'
]

DEFAULT_CONFIG = {
    'apiVersion': 'v1',
    'kind': 'Config',
    'preferences': {},
    'current-context': '',
    'contexts': [],
    'clusters': [],
    'users': []
}

args = None

fileNamePath = os.path.dirname(os.path.realpath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(fileNamePath, "config.yaml")

def loadDefaultYaml():
    try:
        loadYaml(DEFAULT_CONFIG_FILE)
    except Exception as e:
        print(str(e))

def loadYaml(filePath):
    with open(filePath, 'r') as f:
        out = f.read()
        yaml_data = yaml.load(out, Loader=yaml.FullLoader)
        if yaml_data.get('kind', '') != 'Config':
            raise Exception('This file is not a config yaml file')
        for attr in DEFAULT_ATTR:
            yaml_data_attr_list = yaml_data.get(attr, '')
            for each in yaml_data_attr_list:
                attrReader = BaseReader(each.get('name',''), attr[:-1], each.get(attr[:-1], ''))
                DEFAULT_CONFIG[attr].append(attrReader)

def standard():
    """
    去除重复，并且保存为字典列表
    """
    for attr in DEFAULT_ATTR:
        value_list = []
        for value in set(DEFAULT_CONFIG[attr]):
            value_list.append(value.dict)
        DEFAULT_CONFIG[attr] = value_list
    DEFAULT_CONFIG['current-context'] = DEFAULT_CONFIG['contexts'][0].get('name','')

def outputYaml(outputfile):
    with open(outputfile, 'w+') as f:
        yaml.dump(DEFAULT_CONFIG, f)

def main():
    print('Start merging kubeconfigs!!!')
    loadDefaultYaml()

    savefile = DEFAULT_CONFIG_FILE
    if args.add != '' and args.to == '':
        loadYaml(os.path.join(os.path.dirname(os.path.realpath(__file__)), args.add))
    elif args.add == '' and args.to != '':
        raise Exception("No add yaml files. Please set add yaml file with 'to yaml file'")
    elif args.add != '' and args.to != '':
        loadYaml(os.path.join(os.path.dirname(os.path.realpath(__file__)), args.add))
        savefile = os.path.join(os.path.realpath(__file__), args.to)
    else:
        configFileNamePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.directory)
        for filePath in glob.glob(os.path.join(configFileNamePath, '*.yaml')):
            loadYaml(filePath)
        if args.to != '':
            savefile = os.path.join(os.path.realpath(__file__), args.to)

    standard()
    outputYaml(savefile)

    print('Merge succeed !!!')
    print('Total number of contexts: %d' % len(DEFAULT_CONFIG['contexts']))
    print('Current context: %s' % DEFAULT_CONFIG['current-context'])

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="合并kubeconfig文件,用于多集群访问")
    #type是要传入的参数的数据类型  help是该参数的提示信息
    parser.add_argument(
        "-D",
        '-d',
        "--directory",
        dest="directory",
        default="configfile",
        type=str,
        help="the directory of kubeconfigs"
    )

    parser.add_argument(
        "-T",
        "-t",
        '--to',
        dest='to',
        default='',
        type=str,
        help="the merged kubeconfig"
    )

    parser.add_argument(
        "-a",
        "-A",
        '--add',
        dest='add',
        default='',
        type=str,
        help="the kubeconfig need to be added"
    )
    args = parser.parse_args()

    main()
