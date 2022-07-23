import tkinter
import subprocess
import json
import os
import tkinter.messagebox
from FilePathController import FilePathController


class TextEditorSettingsController:
    def __init__(self, currentScriptFolder: str):
        self.settingsFileName = currentScriptFolder + r'\settings-text-editor.json'
        self.settings = {'textEditorPath': ''}
        if os.path.exists(self.settingsFileName):
            settingsFile = open(self.settingsFileName, 'r')
            self.settings = json.load(settingsFile)
            settingsFile.close()

    def getTextEditorPath(self):
        textEditorPath = self.settings['textEditorPath'] if self.settings['textEditorPath'] else FilePathController.getDefaultTextEditorPath()
        return textEditorPath

    def checkAndSavePath(self, textEditorEntry: tkinter.Entry):
        textEditorPath = str(textEditorEntry.get())
        # noinspection PyBroadException
        try:
            subprocess.Popen(textEditorPath)
        except:
            tkinter.messagebox.showwarning("Предупреждение", "Не удалось открыть редактор")
            return

        self.settings['textEditorPath'] = textEditorPath
        settingsFile = open(self.settingsFileName, 'w')
        json.dump(self.settings, settingsFile, indent=4)
        settingsFile.close()
