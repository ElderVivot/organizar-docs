import os
import shutil
from functions import treatTextField


def identifiesWhereFileSaved(settingFiles, pathBaseToSave: str, filePath: str, nameFile: str, companie: str, year: str, month: str):
    nameFileFormated = treatTextField(nameFile)
    for setting in settingFiles:
        try:
            if nameFileFormated.find(setting['patternFile']) >= 0:
                fileDest: str = setting['fileDest']
                fileDest = f'{pathBaseToSave}/{fileDest}'
                fileDest = fileDest.replace('{empresa}', companie).replace('{ano}', year).replace('{mes}', month)
                if filePath.find('resumido') >= 0:
                    nameFile = f'Resumido_{nameFile}'

                if os.path.exists(fileDest) is False:
                    os.makedirs(fileDest)

                fileDest = os.path.join(fileDest, nameFile)
                shutil.move(filePath, fileDest)
                print(f'- Arquivo {nameFile} copiado com sucesso para {fileDest}')
                break
        except Exception as e:
            print(e)
