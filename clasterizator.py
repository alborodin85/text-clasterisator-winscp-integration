from ClusteringObject import ClusteringObject
from FilePathController import FilePathController
from WindowFormController import WindowFormController
from WindowFormEventHandler import WindowFormEventHandler
from SettingsController import SettingsController


def startClustering(logPathLocal):
    startRowRegExp = str(windowFormController.regExpEntry.get())
    settingsController.saveRegExp(startRowRegExp)
    if startRowRegExp and logPathLocal:
        clusteringResult = ClusteringObject().main(logPathLocal, startRowRegExp, windowFormController.window)
        windowFormEventHandler.renderResult(clusteringResult)


currentScriptFolder = FilePathController.getScriptFolder()
clusterTempFile = FilePathController.getClusterTempFilePath()
textEditorPath = r'C:\Program Files\Sublime Text\sublime_text.exe'
logPath = FilePathController.getLogPath()
settingsController = SettingsController(currentScriptFolder, logPath)
startRowRegExpInit = settingsController.getRegExp()

windowFormController = WindowFormController(
    currentScriptFolder=currentScriptFolder,
    windowWidth=700,
    windowHeight=600,
    logPath=logPath,
    startRowRegExpInit=startRowRegExpInit,
    startClusteringCallback=startClustering
)
windowFormEventHandler = WindowFormEventHandler(
    windowWidth=windowFormController.windowWidth,
    windowHeight=windowFormController.windowHeight,
    clusterTempFile=clusterTempFile,
    textEditorPath=textEditorPath,
    windowFormController=windowFormController
)

windowFormController.window.bind("<Configure>", windowFormEventHandler.onWindowChange)
windowFormController.window.protocol("WM_DELETE_WINDOW", windowFormEventHandler.onWindowClose)
windowFormController.openInSublimeButton.bind("<Button-1>", windowFormEventHandler.openInSublime)
windowFormController.messagesListbox.bind('<<ListboxSelect>>', lambda listboxEvent: windowFormEventHandler.messagesListBoxClick(listboxEvent, windowFormController.messageTextBox))
windowFormController.clustersListbox.bind('<<ListboxSelect>>', lambda event: windowFormEventHandler.clustersListboxClick(event))
windowFormController.openClusterInSublimeButton.bind("<Button-1>", lambda buttonEvent: windowFormEventHandler.openClusterInSublime())

windowFormController.window.mainloop()
