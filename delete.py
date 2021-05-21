from view import getFolderId
from common import executequery, getFolderIdUsingParent

def delete(folder):
    pathlist = folder.split('/')
    if len(pathlist) == 1:
        query = "DELETE FROM `folder_structure`.`folders` WHERE (`name` = '%s' and `parent_id`=1);" % (pathlist[0])
    else:
        parentId, name = getFolderId(pathlist[0])
        for f in pathlist[1:]:
            folderId, name = getFolderIdUsingParent(f, parentId)
            parentId = folderId
        query = "DELETE FROM `folder_structure`.`folders` WHERE (`folder_id` = '%d');"%(parentId)
    executequery(query)
    print("Deleted successfully")