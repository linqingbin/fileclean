#-*-coding:utf-8-*-
u'''
Date:20170123
Author:linqingbin
Description:测试fileclean
'''
import os
import shutil
import unittest
import fileclean
reload(fileclean)

def make_files(file_dict,root_path):
    '''
    根据指令生成文件夹

    Parameters
    ----------
    file_dict:dict
        文件夹情况的描述指令
    root_path:string
        根目录位置

    Returns
    -------
    None
    '''
    os.mkdir(root_path)
    for file_name in file_dict.keys():
        file_path = root_path +"/"+ file_name
        value = file_dict[file_name]
        if value == 1:
            with open(file_path,'w') as f:
                pass
        elif isinstance(value,dict):
            make_files(value,file_path)
    return None

def check_files(dir_path):
    '''
    检查文件夹的情况

    Parameters
    ----------
    dir_path:string
        文件夹位置

    Returns
    -------
    file_dict:dict
        文件夹情况的描述
    '''
    file_dict = {}
    filelist = os.listdir(dir_path)
    if len(filelist) == 0:
        return {}
    for file_name in filelist:
        filepath = dir_path+"/"+ file_name
        file_name = file_name.decode('gbk')
        if os.path.isdir(filepath):
            file_dict[file_name] = check_files(filepath)
        else:
            file_dict[file_name] = 1
    return file_dict

def emptydir(dir_path):
    '''清空文件夹'''
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

class TestCase(unittest.TestCase):

    def setUp(self):
        self.root_path = 'G:/Project/softclean/Testcase/case1'
        self.to_path = 'G:/Project/softclean/Testcase/case2'
        self.config_path = 'test_config.csv'
        emptydir(self.to_path)
        if os.path.exists(self.root_path):
            shutil.rmtree(self.root_path)

    def test_delete(self):        
        '''测试文件的遍历删除'''
        dir1_init_dict = {'x.txt':1,'x.txtt':1,'txt':{},'indoor':{'x.txt':1,'y.rar':1},'z.mkv':1}
        dir1_suppose_dict = {'x.txtt':1,'indoor':{'y.rar':1},'txt':{}}
        make_files(dir1_init_dict,self.root_path)
        fileclean.main(self.config_path)
        self.assertEqual(check_files(self.root_path),dir1_suppose_dict)

    def test_move(self):
        '''测试文件的遍历移动'''
        dir1_init_dict = {'z.mkv':1,'l.mkv':1,'z.avi':1,'mkv.mkvv':1,'txt':{},'indoor':{'y.rar':1,'f.mkv':1}}
        dir2_suppose_dict = {'z.mkv':1,'l.mkv':1}
        make_files(dir1_init_dict,self.root_path)
        fileclean.main(self.config_path)
        self.assertEqual(check_files(self.to_path),dir2_suppose_dict)

    def test_copy(self):
        '''测试文件的遍历复制'''
        dir1_init_dict = {'1.doc':1,'txt':{},'indoor':{'2.doc':1,'3.xdoc':1}}
        dir1_suppose_dict = {'1.doc':1,'txt':{},'indoor':{'2.doc':1,'3.xdoc':1}}
        dir2_suppose_dict = {'1.doc':1,'2.doc':1}
        make_files(dir1_init_dict,self.root_path)
        fileclean.main(self.config_path)
        self.assertEqual(check_files(self.root_path),dir1_suppose_dict)
        self.assertEqual(check_files(self.to_path),dir2_suppose_dict)

    def tearDown(self):
        emptydir(self.root_path)
        emptydir(self.to_path)

if __name__ == '__main__':
    unittest.main()















