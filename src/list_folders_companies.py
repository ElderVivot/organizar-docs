from typing import Dict
import os


def listFoldersCompanies(pathBaseToSave: str) -> Dict[str, str]:
    listFolders = {}

    for nameFolder in os.listdir(pathBaseToSave):
        nameFolderSplit = nameFolder.split('-')
        codeCompanie = nameFolderSplit[-1].strip()
        listFolders[codeCompanie] = nameFolder

    return listFolders
