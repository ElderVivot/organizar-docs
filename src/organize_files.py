import os
from typing import Dict
from identifies_where_file_saved import identifiesWhereFileSaved
from functions import treatNumberField


def organizeFiles(pathBaseFilesSavedRoutine: str, listFoldersDest: Dict[str, str], pathBaseToSave: str, settingFiles) -> None:
    listDir = os.listdir(pathBaseFilesSavedRoutine)

    qtdFiles = 0
    for nameFile in listDir:
        try:
            filePath = os.path.join(pathBaseFilesSavedRoutine, nameFile)
            if os.path.isdir(filePath) is True:
                continue
            qtdFiles += 1
            nameFileSplit = nameFile.split('_')
            codeCompanie = nameFileSplit[1]
            codeCompanieAsNumber = treatNumberField(codeCompanie, isInt=True)
            if codeCompanieAsNumber <= 0:
                print(f'- Arquivo {nameFile} não possui código da empresa após o primeiro underline.')
                continue
            monthYear = nameFileSplit[2]
            year = monthYear[2:6]
            month = monthYear[0:2]
            companie = listFoldersDest[codeCompanie]

            identifiesWhereFileSaved(settingFiles, pathBaseToSave, filePath, nameFile, companie, year, month)
        except Exception as e:
            print(f'- Erro ao copiar arquivo {nameFile}, o erro é {e}')

    if qtdFiles == 0:
        print(f'- Não existe arquivos na pasta {pathBaseFilesSavedRoutine} à serem processados.')
