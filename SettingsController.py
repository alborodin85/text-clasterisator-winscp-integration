import json
import os
import re
import subprocess
import tkinter.messagebox


class SettingsController:
    def __init__(self, currentScriptFolder: str, logPath: str, textEditorPath: str):
        self.logPath = logPath.replace('\\', '/')
        self.settingsFileName = currentScriptFolder + r'\settings.json'

        self.startRowRegExp = ''
        self.algorithmIdValue = 1
        self.countClustersValue = 1
        self.countRowsValue = 0

        self.settings = []
        self.textEditorPath = textEditorPath
        if os.path.exists(self.settingsFileName):
            settingsFile = open(self.settingsFileName, 'r')
            self.settings = json.load(settingsFile)
            settingsFile.close()
            self.__parseSettingsFile()
        else:
            settingsFile = open(self.settingsFileName, 'w')
            settingsFile.close()

    def openSettingsInEditor(self):
        # noinspection PyBroadException
        try:
            subprocess.Popen([self.textEditorPath, self.settingsFileName])
        except:
            tkinter.messagebox.showwarning("Предупреждение", "Не удалось открыть редактор")

    def getRegExp(self) -> str:
        return self.startRowRegExp

    def getAlgorithmId(self) -> int:
        return self.algorithmIdValue

    def getCountClusters(self) -> int:
        return self.countClustersValue

    def getCountRows(self) -> int:
        return self.countRowsValue

    def saveAlgorithmId(self, algorithmIdValue: int):
        self.algorithmIdValue = algorithmIdValue
        self.__saveToFile('algorithmId', str(self.algorithmIdValue))

    def saveRegExp(self, startRowRegExp: str):
        self.startRowRegExp = startRowRegExp
        self.__saveToFile('regExp', str(self.startRowRegExp))

    def saveCountClusters(self, countClustersValue: int):
        self.countClustersValue = countClustersValue
        self.__saveToFile('countClustersValue', str(self.countClustersValue))

    def saveCountRows(self, countRowsValue: int):
        self.countRowsValue = countRowsValue
        self.__saveToFile('countRowsValue', str(self.countRowsValue))

    def __saveToFile(self, settingsName: str, settingsValue: str):
        isSettingsExists = False
        for i in range(len(self.settings)):
            if self.__isSettingsFit(self.settings[i]):
                self.settings[i][settingsName] = settingsValue
                isSettingsExists = True
                break
        if not isSettingsExists:
            self.settings.append({
                'path': self.__getSettingsLogPath(),
                settingsName: self.startRowRegExp
            })

        settingsFile = open(self.settingsFileName, 'w')
        json.dump(self.settings, settingsFile, indent=4)
        settingsFile.close()

    def __parseSettingsFile(self):
        for settingsItem in self.settings:
            if self.__isSettingsFit(settingsItem):
                self.startRowRegExp = settingsItem['regExp']
                self.algorithmIdValue = int(settingsItem['algorithmId']) if 'algorithmId' in settingsItem else 1
                self.countClustersValue = int(settingsItem['countClustersValue']) if 'countClustersValue' in settingsItem else 1
                self.countRowsValue = int(settingsItem['countRowsValue']) if 'countRowsValue' in settingsItem else 0
                break

    def __isSettingsFit(self, settingsItem: dict):
        logPathItems = self.logPath.split('/')
        logPathItemsCount = len(logPathItems)
        settingsLogPathItems = settingsItem['path'].split('/')
        settingsLogPathItemsCount = len(settingsLogPathItems)
        isSettingsFit = True
        for j in range(logPathItemsCount - 1, -1, -1):
            logPathElem = logPathItems[j]
            if j > (logPathItemsCount - settingsLogPathItemsCount):
                settingsLogPathElem = settingsLogPathItems[j - logPathItemsCount + settingsLogPathItemsCount]
                if not re.fullmatch(settingsLogPathElem, logPathElem):
                    isSettingsFit = False
        return isSettingsFit

    def __getSettingsLogPath(self):
        settingsLogPath = ''
        settingsLogPathItems = []
        logPathItems = self.logPath.split('/')
        for i in range(len(logPathItems) - 1, -1, -1):
            if re.fullmatch(r'scp\d+', logPathItems[i]):
                break
            settingsLogPathItems.append(f'/{logPathItems[i]}')

        for i in range(len(settingsLogPathItems) - 1, -1, -1):
            settingsLogPath += settingsLogPathItems[i]

        return settingsLogPath
