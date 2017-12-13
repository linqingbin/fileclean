#-*-coding:utf-8-*-
'''
Date:20170116
Author:linqingbin
Description:文件清理
'''

import os
import re
import time
import shutil

def cleanwork(from_path,to_path,pattern,command,iscrawl=False):
    '''
    清理指定文件夹的文件

    Parameters
    ----------
    from_path:string
        目标文件夹
    to_path:string
        转移到的文件夹
    pattern:string
        匹配文件用的正则表达式
    command:string
        操作类型：支持delete、move和copy
    iscrawl:bool,default is False
        是否对文件夹进行爬取

    Returns
    -------
    None
    '''
    filelist = os.listdir(from_path)
    to_path_file_list = []
    if command in ('move','copy'):
        to_path_file_list = os.listdir(to_path)
    for i in filelist:
        filepath = from_path+"/"+i
        if os.path.isdir(filepath) and bool(int(iscrawl)): # 处理对文件夹的递归问题
            cleanwork(filepath,to_path,pattern,command,iscrawl)
        else:
            if re.match(pattern,i):
                if command == 'delete':
                    os.remove(filepath)
                elif i in to_path_file_list: # 处理移动类的指令
                    continue
                else:
                    if command == 'move':
                        shutil.move(filepath,to_path)
                    elif command == 'copy':
                        shutil.copy(filepath,to_path)
                print("{0} To {1} {2} done".format(filepath,to_path,command))

def main(config_path):
    with open(config_path,'r') as f:
        config = f.read()
    works = [x.split(',') for x in config.split('\n')][1:]  # 获取任务
    for work in works:  # 逐个执行任务
        if len(work) == 5:
            from_path,to_path,pattern,command,iscrawl = work
            cleanwork(from_path,to_path,pattern,command,iscrawl)

if __name__ == '__main__':
    config_path = 'config/config.csv'
    print('file start!')
    main(config_path)
    print('file end!')
