import os
from typing import Dict
from identifies_where_file_saved import identifiesWhereFileSaved


def organizeFiles(nameFolder: str, listFoldersDest: Dict[str, str]) -> None:
    for nameFile in os.listdir(nameFolder):
        filePath = os.path.join(nameFolder, nameFile)
        if os.path.isdir(filePath) is True:
            continue
        nameFileSplit = nameFile.split('_')
        codeCompanie = nameFileSplit[1]
        monthYear = nameFileSplit[2]
        year = monthYear[2:6]
        month = monthYear[0:2]
        companie = listFoldersDest[codeCompanie]

        identifiesWhereFileSaved(filePath, nameFile, companie, year, month)
