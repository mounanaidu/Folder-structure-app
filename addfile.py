'''This files contains all the functionalities to add files and folders'''

import datetime, os
from common import getFileMeta, executequery

def insertDatafile(parent_id, folder, file_ctime, file_mtime, file_size, file_type):
    query = "INSERT INTO `folder_structure`.`folders` (`parent_id`, `name`, `created_time`, `updated_time`, `size`, `type`) VALUES ('%d', '%s', '%s', '%s', '%d', '%s');" % (
        parent_id, folder, file_ctime, file_mtime, file_size, file_type)
    executequery(query)

def checkDataDup(folder):
    checkQuery = "SELECT * FROM folder_structure.folders where name='%s' and parent_id=1;" % (folder)
    result = executequery(checkQuery)
    if result.fetchone():
        print("same folder already exists")
        return True
    else:
        return False

def insertData(folder,path,parent_id, is_root):
    file_size, file_ctime, file_mtime = getFileMeta(path)
    file_type = getFileType(folder)
    dataExists = checkDataDup(folder)
    if dataExists:
        return False
    if is_root:
        if file_type:
            insertDatafile(1, folder, file_ctime, file_mtime, file_size, file_type)
        else:
            query = "INSERT INTO `folder_structure`.`folders` (`parent_id`, `name`, `created_time`, `updated_time`, `size`) VALUES ('%d', '%s', '%s', '%s', '%d');" % (
                1, folder, file_ctime, file_mtime, file_size)
            executequery(query)
    else:
        if file_type:
            insertDatafile(parent_id[0], folder, file_ctime, file_mtime, file_size, file_type)
        else:
            query = "INSERT INTO `folder_structure`.`folders` (`parent_id`, `name`, `created_time`, `updated_time`, `size`) VALUES ('%d', '%s', '%s', '%s', '%d');" % (
                parent_id[0], folder, file_ctime, file_mtime, file_size)
            executequery(query)
    return True

def addDirectory(file, folderPath):
    file = file.split('/')[-1]
    rootInserted = insertData(file, folderPath, 1, True)
    if not rootInserted:
        exit()
    for root, d_names, f_names in os.walk(folderPath):
        #add directories
        for d in d_names:
            parent_folder = root.split('\\')[-1]
            query = "select folder_id from folder_structure.folders where name='%s';"%(parent_folder)
            cursor = executequery(query)
            parent_id = cursor.fetchone()
            insertData(d, root+'\\'+d, parent_id, False)

        #add files
        for f in f_names:
            root = root.replace('/','\\')
            parent_folder = root.split('\\')[-1]
            # parent_folder = root.split('/')[-1]
            query = "select folder_id from folder_structure.folders where name='%s';"%(parent_folder)
            cursor = executequery(query)
            parent_id = cursor.fetchone()
            insertData(f, root+'\\'+f, parent_id, False)

def addFile(folder, file, file_type):
    file = file.split('/')[-1]
    file_size, file_ctime, file_mtime = getFileMeta(folder)
    insertDatafile(1, file, file_ctime, file_mtime, file_size, file_type)

def getFileType(file):
    split_tup = file.split('.')
    if len(split_tup) > 1:
        file_name = split_tup[0]
        file_extension = split_tup[1]
        return file_extension
    else:
        return False

def add(folderPath):
    file = folderPath.split('\\')[-1]
    addType = getFileType(folderPath)
    if addType:
        addFile(folderPath, file, addType)
    else:
        addDirectory(file, folderPath)

    print("Added successfully")
