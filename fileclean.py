#-*-coding:utf-8-*-
u'''
Date:20170116
Author:linqingbin
Description:文件清理
'''

import os
import re
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
            # print "%s is crawled!" % filepath
            cleanwork(filepath,to_path,pattern,command,iscrawl)
        else:
            if re.match(pattern,i):
                if command == 'delete':
                    os.remove(filepath)
                elif filepath not in to_path_file_list: # 处理移动类的指令
                    if command == 'move':
                        shutil.move(filepath,to_path)
                    elif command == 'copy':
                        shutil.copy(filepath,to_path)
                else:
                    break

def main(config_path):
    with open(config_path,'r') as f:
        config = f.read().decode('gbk')
    works = [x.split(',') for x in config.split('\n')][1:]  # 获取任务
    for work in works:  # 逐个执行任务
        if len(work) == 5:
            from_path,to_path,pattern,command,iscrawl = work
            cleanwork(from_path,to_path,pattern,command,iscrawl)
            # print "File match %s has been moved from %s . "% (pattern,from_path)

config_path = 'config.csv'

if __name__ == '__main__':
    main(config_path)