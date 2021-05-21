
import os
import datetime
import MySQLdb

def getFileMeta(file):
    file_size = os.path.getsize(file)
    file_ctime = datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime('%Y-%m-%d %H:%M:%S')
    file_ctime = datetime.datetime.strptime(file_ctime, '%Y-%m-%d %H:%M:%S')
    file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
    file_mtime = datetime.datetime.strptime(file_mtime, '%Y-%m-%d %H:%M:%S')
    return file_size, file_ctime, file_mtime

def getFolderIdUsingParent(folderName, parentId):
    query = "select folder_id, name from folder_structure.folders where name = '%s' and parent_id = '%d';" % (folderName, parentId)
    cursor = executequery(query)
    folder_id, name = cursor.fetchone()
    return folder_id, name

def executequery(query):
    db = MySQLdb.connect("localhost", "root", "root", "folder_structure")
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()

    return cursor