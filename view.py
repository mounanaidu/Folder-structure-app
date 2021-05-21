from common import executequery

def viewroot():
    query = "select folder_id, name, created_time from folder_structure.folders where parent_id='%s';"%(1)
    cursor = executequery(query)
    data = cursor.fetchall()
    print("FOLDER" + ' '*5 + '|'+' '*5 + "CREATED TIME")
    print('---'*20)
    for sdata in data:
        print(sdata[1] + ' '*5 + '|'+' '*5 + str(sdata[2]))

def getFolderId(folderName):
    query = "select folder_id, name from folder_structure.folders where name = '%s';"%(folderName)
    cursor = executequery(query)
    folder_id, name = cursor.fetchone()
    return folder_id, name

def getChildwithParentId(folder_id):
    query = "select folder_id, name, size, type from folder_structure.folders where parent_id = '%s';"%(folder_id)
    cursor = executequery(query)
    data = cursor.fetchall()
    return data


def view(folder, folderDict):
    folders = folder.split('/')
    folderName = folders[-1]
    folder_id, name = getFolderId(folderName)
    subfolders = getChildwithParentId(folder_id)

    if subfolders:
        for folder in subfolders:
            if folder[3] is None:
                folderDict[folder[1]] = {}
                view(folder[1],folderDict[folder[1]])
            else:
                folderDict[folder[1]] = [folder[2], folder[3]]
    resultDict = {name: folderDict}
    return resultDict

def printView(resultDict, counter):
    for k,v in resultDict.items():
        if type(v) == list:
            print(' '*counter +'|-', k,' ',v)
        else:
            print(' ' * counter +'|-', k)
            if v:
                counter += 5
                printView(v, counter)
                counter -= 5
