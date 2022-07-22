from ClusteringObject import ClusteringObject
from FilePathController import FilePathController
from WindowFormController import WindowFormController
from WindowFormEventHandler import WindowFormEventHandler


def startClustering(logPathLocal):
    startRowRegExpLocal = str(windowFormController.regExpEntry.get())
    clusteringResult = ClusteringObject().main(logPathLocal, startRowRegExpLocal, windowFormController.window)
    windowFormEventHandler.renderResult(clusteringResult, windowFormController)


currentScriptFolder = FilePathController.getScriptFolder()
clusterTempFile = FilePathController.getClusterTempFilePath()
textEditorPath = r'C:\Program Files\Sublime Text\sublime_text.exe'
windowFormController = WindowFormController(currentScriptFolder=currentScriptFolder, windowWidth=700, windowHeight=600)
windowFormEventHandler = WindowFormEventHandler(windowFormController.windowWidth, windowFormController.windowHeight, clusterTempFile, textEditorPath)
windowFormController.window.bind("<Configure>", windowFormEventHandler.onWindowChange)
windowFormController.window.protocol("WM_DELETE_WINDOW", windowFormEventHandler.onWindowClose)

logPath = FilePathController.getLogPath()
windowFormController.buildTopContainer(logPath)
windowFormController.openInSublimeButton.bind("<Button-1>", windowFormEventHandler.openInSublime)

startRowRowRegExpInit = r'\d{4}-\d{2}-\d{2} {1,2}\d{1,2}:\d{2}:\d{2}'
windowFormController.buildRegExpContainer(startRowRowRegExpInit, lambda: startClustering(logPath))

windowFormController.buildBodyContainer()
windowFormController.buildSearchContainer()

windowFormController.window.mainloop()
