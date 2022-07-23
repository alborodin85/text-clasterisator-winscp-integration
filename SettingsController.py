import json
import os
import re


class SettingsController:
    def __init__(self, currentScriptFolder: str, logPath: str):
        self.logPath = logPath.replace('\\', '/')
        self.settingsFileName = currentScriptFolder + r'\settings.json'
        self.startRowRegExp = ''
        self.settings = []
        if os.path.exists(self.settingsFileName):
            settingsFile = open(self.settingsFileName, 'r')
            self.settings = json.load(settingsFile)
            settingsFile.close()
            self.__parseSettingsFile()
        else:
            settingsFile = open(self.settingsFileName, 'w')
            settingsFile.close()

    def __parseSettingsFile(self):
        for settingsItem in self.settings:
            if self.__isSettingsFit(settingsItem):
                self.startRowRegExp = settingsItem['regExp']
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
        for i in range(len(logPathItems)-1, -1, -1):
            if re.fullmatch(r'scp\d+', logPathItems[i]):
                break
            settingsLogPathItems.append(f'/{logPathItems[i]}')

        for i in range(len(settingsLogPathItems)-1, -1, -1):
            settingsLogPath += settingsLogPathItems[i]

        return settingsLogPath

    def getRegExp(self):
        return self.startRowRegExp

    def saveRegExp(self, startRowRegExp: str):
        self.startRowRegExp = startRowRegExp
        isSettingsExists = False
        for i in range(len(self.settings)):
            if self.__isSettingsFit(self.settings[i]):
                self.settings[i]['regExp'] = self.startRowRegExp
                isSettingsExists = True
                break
        if not isSettingsExists:
            self.settings.append({
                'path': self.__getSettingsLogPath(),
                'regExp': self.startRowRegExp
            })

        settingsFile = open(self.settingsFileName, 'w')
        json.dump(self.settings, settingsFile, indent=4)
        settingsFile.close()
