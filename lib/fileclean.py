# -*-coding:utf-8-*-
'''
Date:20170116
Author:linqingbin
Description:File clean
'''
import time
import os
import re
import shutil
import logging

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S', filename='log.log', level="DEBUG")


def cleanwork(from_path, to_path, pattern, command, iscrawl=False, iter_times=0):
    '''
    File clean up

    Parameters
    ----------
    from_path:string
        Source folder
    to_path:string
        Target folder
    pattern:string
        Regular expression partern for file match
    command:string
        delete, move or copy
    iscrawl:bool,default is False
        is crawl fodler if exists nesting folders

    Returns
    -------
    None
    '''
    task_name = "Task {0} {2} to {1} ".format(from_path, to_path, command)
    logging.info('{task} start'.format(task=task_name))
    try:
        filelist = os.listdir(from_path)
    except Exception:
        logging.error("Open %s error." % from_path)
        return None
    to_path_file_list = []
    if command in ('move', 'copy'):
        to_path_file_list = os.listdir(to_path)
    for filename in filelist:
        filepath = from_path + "/" + filename
        # Handling recursive problems with folders
        if os.path.isdir(filepath) and bool(int(iscrawl)) and iter_times < 10:
            iter_times += 1
            logging.info(filepath, iter_times)
            cleanwork(filepath, to_path, pattern, command, iscrawl, iter_times)
        elif re.match(pattern, filename, flags=re.IGNORECASE):
            if command == 'delete':
                os.remove(filepath)
            elif filename in to_path_file_list:
                continue
            else:
                if command == 'move':
                    shutil.move(filepath, to_path)
                elif command == 'copy':
                    shutil.copy(filepath, to_path)
            logging.info('{task} done'.format(task=task_name))
    # logging.info('{task} end'.format(task=task_name))


def main(tasks_path):
    logging.info("Program start")
    with open(tasks_path, 'r') as f:
        tasks = f.read()
    works = [x.split(',') for x in tasks.split('\n')][1:]  # Get tasks
    logging.info("{n} tasks found".format(n=len(works)))
    for work in works:
        if len(work) == 5:
            from_path, to_path, pattern, command, iscrawl = work
            cleanwork(from_path, to_path, pattern, command, iscrawl)
    logging.info("Program end")
