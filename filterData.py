from common import executequery
import re

def getFolderId(folderName):
    query = "select folder_id, name from folder_structure.folders where name = '%s';" % (folderName)
    cursor = executequery(query)
    folder_id, name = cursor.fetchone()
    return folder_id, name

def getChildwithParentId(folder_id, column, value):
    query = "select folder_id, name, size, type from folder_structure.folders where parent_id = '%s';" % (folder_id)
    cursor = executequery(query)
    data = cursor.fetchall()
    return data

def filterData(folder, folderDict, column, value):
    folders = folder.split('/')
    folderName = folders[-1]
    folder_id, name = getFolderId(folderName)
    subfolders = getChildwithParentId(folder_id, column, value)

    if subfolders:
        for folder in subfolders:
            if folder[3] is None:
                folderDict[folder[1]] = {}
                filterData(folder[1], folderDict[folder[1]], column, value)
            else:
                if column == '-type':
                    result = re.match(value, folder[3])
                    if result:
                        folderDict[folder[1]] = [folder[2], folder[3]]
                elif column == '-name':
                    result = re.match(value, folder[1])
                    if result:
                        folderDict[folder[1]] = [folder[2], folder[3]]

    resultDict = {name: folderDict}
    resultDict = removeEmptyDict(resultDict)
    return resultDict

def removeEmptyDict(data):
    new_data = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = removeEmptyDict(v)
        if not v in (u'', None, {}):
            new_data[k] = v
    return new_data

def printFilter(resultDict, counter):
    for k, v in resultDict.items():
        if type(v) == list:
            print(' ' * counter + '|-', k, ' ', v)
        elif not v:
            return
        else:
            print(' ' * counter + '|-', k)
            if v:
                counter += 5
                printFilter(v, counter)
                counter -= 5
