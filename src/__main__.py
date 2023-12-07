import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from functions import returnDataInDictOrArray
from list_folders_companies import listFoldersCompanies
from organize_files import organizeFiles
from images import PLUS_ICO, NEGATIVE_ICO, HELP_ICO


def local_path():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path('.')


folderSrc = local_path()
sys.path.append(folderSrc)
print(folderSrc)

fileJson = os.path.join("C:/autmais/organizar-docs", 'env.json')
dataEnv = json.load(open(fileJson))
pathBaseFilesSavedRoutine = dataEnv['pathBaseFilesSavedRoutine']


import PySimpleGUI as sg


class MainProject():
    def __init__(self) -> None:
        self.__pathBaseFilesSavedRoutine: str = returnDataInDictOrArray(dataEnv, ['pathBaseFilesSavedRoutine'])
        self.__pathBaseToSave: str = returnDataInDictOrArray(dataEnv, ['pathBaseToSave'])
        self.__linesPatternFile: List[Dict[str, Any]] = returnDataInDictOrArray(dataEnv, ['files'], [])
        self.__numberRow = 0
        self.__rowsLinesPatternFileDeleted = []

    def __updateVariables(self, values):
        folderOriginal = returnDataInDictOrArray(values, ['-folderOriginal-'], None)
        folderToSave = returnDataInDictOrArray(values, ['-folderToSave-'], None)
        self.__pathBaseFilesSavedRoutine = self.__pathBaseFilesSavedRoutine if folderOriginal is None else folderOriginal
        self.__pathBaseToSave = self.__pathBaseToSave if folderToSave is None else folderToSave

        print(values)
        self.__linesPatternFile = []
        for numberLine in range(0, self.__numberRow):
            if self.__rowsLinesPatternFileDeleted.count(numberLine) == 0:
                self.__linesPatternFile.append({
                    "patternFile": values[('-patternFile-', numberLine)],
                    "fileDest": values[('-fileDest-', numberLine)]
                })

    def __linePatternFileMethod(self, numberRow: int, patternFile: str, fileDest: str):
        return [sg.pin(
            sg.Col([[
                sg.T("Nome Arquivo: "), sg.InputText(patternFile, size=(25, 5), key=("-patternFile-", numberRow)),
                sg.T("Local pra Salvar:"), sg.InputText(fileDest, size=(65, 5), key=("-fileDest-", numberRow)),
                sg.Button(enable_events=True, image_data=NEGATIVE_ICO, key=("-DEL-", numberRow))]],
                key=('-ROW-', numberRow)
            ))]

    def __addLinePatternFile(self, numberRow: int, patternFile='', fileDest=''):
        return [self.__linePatternFileMethod(numberRow, patternFile, fileDest)]

    def __showLinesPatternAlreadySaved(self):
        if len(self.__linesPatternFile) == 0:
            return self.__addLinePatternFile(0, '', '')
        else:
            arrayElemens = []
            for linePattern in self.__linesPatternFile:
                arrayElemens.append(self.__linePatternFileMethod(self.__numberRow, linePattern['patternFile'], linePattern['fileDest']))
                self.__numberRow += 1
            return arrayElemens

    def __updateFileSettings(self, values):
        try:
            self.__updateVariables(values)
            dataEnv['pathBaseFilesSavedRoutine'] = self.__pathBaseFilesSavedRoutine
            dataEnv['pathBaseToSave'] = self.__pathBaseToSave
            dataEnv['files'] = self.__linesPatternFile
            with open(fileJson, 'w') as outfile:
                outfile.write(json.dumps(dataEnv, indent=4))
        except Exception as e:
            print(f'Error ao salvar alterações {e}')

    def main(self):
        sg.theme('Dark Grey 13')

        tab1 = [
            [sg.Text('Caminho da rotina automática:'), sg.InputText(self.__pathBaseFilesSavedRoutine, size=(60, 5),
                                                                    key='-folderOriginal-'), sg.FolderBrowse('Procurar', initial_folder=self.__pathBaseFilesSavedRoutine)],
            [sg.Text('Caminho pra mover arquivos:'), sg.InputText(self.__pathBaseToSave, size=(60, 5), key='-folderToSave-'), sg.FolderBrowse('Procurar', initial_folder=self.__pathBaseFilesSavedRoutine)],
            [sg.Button('Processar'), sg.Button('Salvar Alterações', key='-salvar_alteracoes-')],
            [sg.Output(size=(700, 500))]
        ]

        tab2 = [
            [sg.Text(), sg.Button(enable_events=True, image_data=PLUS_ICO, key="-plus-"), sg.Text(), sg.Button(enable_events=True, image_data=HELP_ICO, key="-help-")],
            [sg.Column(self.__showLinesPatternAlreadySaved(), key='-Column-')]
        ]

        layout = [[sg.TabGroup([[
            sg.Tab('Inicial', tab1),
            sg.Tab('Mapear Pastas', tab2)
        ]])]]

        window = sg.Window('Organizador de Arquivos Rotina Automática Domínio', layout, size=(960, 500), finalize=True)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Fechar':
                break

            # add new line in patternFile
            if event == '-plus-':
                window.extend_layout(window['-Column-'], self.__addLinePatternFile(self.__numberRow, '', ''))
                self.__numberRow += 1

            # delete line in patternFile
            if event[0] == '-DEL-':
                window[('-ROW-', event[1])].update(visible=False)
                self.__rowsLinesPatternFileDeleted.append(event[1])

            if event == '-salvar_alteracoes-':
                self.__updateFileSettings(values)

            if event == '-help-':
                sg.popup(
                    'Preencher com texto fixo + {nome_pasta_variavel}. \nExemplo, supondo que você queira que o arquivo vá pra pasta "EMPRESA ABC/DP FISCAL/2023/10/DAS". Portanto, deverá configurar como "{empresa}/DP FISCAL/{ano}/{mes}/DAS".')

            if event == 'Processar':
                try:
                    self.__updateFileSettings(values)

                    listFoldersDest = listFoldersCompanies(self.__pathBaseToSave)
                    organizeFiles(self.__pathBaseFilesSavedRoutine, listFoldersDest, self.__pathBaseToSave, self.__linesPatternFile)
                    organizeFiles(f'{self.__pathBaseFilesSavedRoutine}/resumido', listFoldersDest, self.__pathBaseToSave, self.__linesPatternFile)
                except Exception as e:
                    print(e)
                    print('Erro ao mover arquivos, o erro é ', e)

        window.close()


MainProject().main()
