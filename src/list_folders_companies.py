from typing import Dict
import os
import sys
import json

folderSrc = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(folderSrc)

dataEnv = json.load(open(os.path.join(folderSrc, 'env.json')))
pathBaseToSave = dataEnv['pathBaseToSave']


def listFoldersCompanies(nameFolder: str) -> Dict[str, str]:
    listFolders = {}

    for nameFolder in os.listdir(pathBaseToSave):
        nameFolderSplit = nameFolder.split('-')
        codeCompanie = nameFolderSplit[-1].strip()
        listFolders[codeCompanie] = nameFolder

    return listFolders
