import os
import sys
import json
from list_folders_companies import listFoldersCompanies
from organize_files import organizeFiles

folderSrc = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(folderSrc)

dataEnv = json.load(open(os.path.join(folderSrc, 'env.json')))
pathBaseFilesSavedRoutine = dataEnv['pathBaseFilesSavedRoutine']


listFoldersDest = listFoldersCompanies('data/processed')
organizeFiles(pathBaseFilesSavedRoutine, listFoldersDest)
organizeFiles(f'{pathBaseFilesSavedRoutine}/resumido', listFoldersDest)
