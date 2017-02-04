#-*-coding:utf-8
'''
日期：2016年6月11日
作者：林庆斌
描述：系统文件的整理
'''

import os
import re
import shutil

def cleansoft():
    path = u"D:/源文件仓库/软件区"
    filelist = os.listdir(path)
    for i in filelist:
        filepath = path+"/"+i
        if re.search(".*\.torrent",i):
            os.remove(filepath)
        elif re.search(".*\.(mp4|mkv|avi)$",i):
            Topath = u"D:/源文件仓库/动画区"
            shutil.move(filepath,Topath)
        elif re.search(".*\.pdf",i):
            Topath = u"F:/书籍"
            shutil.move(filepath,Topath)
        elif os.path.isdir(filepath):
            if len(os.listdir(filepath)) == 0:
                os.rmdir(filepath)

def cleanpath(path,filelike):
    '''清楚文件夹下指定类型的文件'''
    filelist = os.listdir(path)
    for i in filelist:
        filepath = path+"/"+i
        if os.path.isdir(filepath):
            print "%s is crawled!" % filepath
            cleanpath(filepath,filelike)
        elif re.search(filelike,i):
            os.remove(filepath)
            print "%s is removed!" % filepath

from_rootpath = u'G:/'
to_rootpath = u'D:/档案馆/141104 文本遗产'

dirnames = [u'生活', u'技术', u'爱好', u'哲学']
def copytxt():
    for i in dirnames:
        from_path = u'%s/%s/待处理文本' % (from_rootpath,i)
        to_path = u'%s/%s' % (to_rootpath,i)
        to_path_file_list = os.listdir(to_path)
        for txt in os.listdir(from_path):
            if txt in to_path_file_list:
                continue
            else:
                file_path = u'%s/%s' % (from_path,txt)
                shutil.copy(file_path,to_path)

def main():
    cleansoft()
    cleanpath(u"G:\Project",".*\.pyc")
    copytxt()

if __name__ == '__main__':
    main()




