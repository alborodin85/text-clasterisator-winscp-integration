from ClusteringObject import ClusteringObject
from FilePathController import FilePathController
from WindowFormController import WindowFormController
from WindowFormEventHandler import WindowFormEventHandler


def startClustering(logPathLocal):
    startRowRegExpLocal = str(windowFormController.regExpEntry.get())
    clusteringResult = ClusteringObject().main(logPathLocal, startRowRegExpLocal, windowFormController.window)
    windowFormEventHandler.renderResult(clusteringResult)


currentScriptFolder = FilePathController.getScriptFolder()
clusterTempFile = FilePathController.getClusterTempFilePath()
textEditorPath = r'C:\Program Files\Sublime Text\sublime_text.exe'
startRowRowRegExpInit = r'\d{4}-\d{2}-\d{2} {1,2}\d{1,2}:\d{2}:\d{2}'
logPath = FilePathController.getLogPath()

windowFormController = WindowFormController(
    currentScriptFolder=currentScriptFolder,
    windowWidth=700,
    windowHeight=600,
    logPath=logPath,
    startRowRowRegExpInit=startRowRowRegExpInit,
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
