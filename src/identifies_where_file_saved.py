import os
import shutil
import sys
import json
from functions import treatTextField

folderSrc = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(folderSrc)

dataEnv = json.load(open(os.path.join(folderSrc, 'env.json')))
settingFiles = dataEnv['files']
pathBaseToSave = dataEnv['pathBaseToSave']


def identifiesWhereFileSaved(filePath: str, nameFile: str, companie: str, year: str, month: str):
    nameFileFormated = treatTextField(nameFile)
    for setting in settingFiles:
        try:
            if nameFileFormated.find(setting['patternFile']) >= 0:
                fileDest: str = setting['fileDest']
                fileDest = f'{pathBaseToSave}/{fileDest}'
                fileDest = fileDest.replace('{companie}', companie).replace('{year}', year).replace('{month}', month)
                if filePath.find('resumido') >= 0:
                    nameFile = f'Resumido_{nameFile}'
                # print(filePath, fileDest)

                if os.path.exists(fileDest) is False:
                    os.makedirs(fileDest)

                fileDest = os.path.join(fileDest, nameFile)
                shutil.move(filePath, fileDest)
                break
        except Exception as e:
            print(e)
