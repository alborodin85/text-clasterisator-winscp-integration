import tkinter
import tkinter.messagebox
import os
import subprocess
import sys
import numpy
import pandas
from ClusteringResult import ClusteringResult
from WindowFormController import WindowFormController


class WindowFormEventHandler:
    def __init__(self, windowWidth: int, windowHeight: int, clusterTempFile: str, windowFormController: WindowFormController, textEditorEntry: tkinter.Entry):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.clusterTempFile = clusterTempFile
        self.windowFormController = windowFormController
        self.selectedCluster = 0
        self.clusteringResult = ClusteringResult(numpy.zeros(1), [], [], [], numpy.zeros(1), pandas.Series([], dtype=object))
        self.textEditorEntry = textEditorEntry

    def onWindowChange(self, event: tkinter.Event):
        self.windowWidth = event.width
        self.windowHeight = event.height

    def onWindowClose(self):
        if os.path.exists(self.clusterTempFile):
            os.remove(self.clusterTempFile)
        quit()

    def openInSublime(self, needQuit=False):
        # noinspection PyBroadException
        try:
            subprocess.Popen([str(self.textEditorEntry.get()), sys.argv[1]])
            if needQuit:
                quit()
        except:
            tkinter.messagebox.showwarning("Предупреждение", "Не удалось открыть редактор")

    def openClusterInSublime(self):
        if not self.clusteringResult.clustersItems:
            return
        f = open(self.clusterTempFile, 'w')
        for messageId in self.clusteringResult.clustersItems[self.selectedCluster]:
            f.write(self.clusteringResult.texts[messageId])
        f.close()
        # noinspection PyBroadException
        try:
            subprocess.Popen([str(self.textEditorEntry.get()), self.clusterTempFile])
        except:
            tkinter.messagebox.showwarning("Предупреждение", "Не удалось открыть редактор")

    def renderResult(self, clusteringResult: ClusteringResult):
        self.clusteringResult = clusteringResult
        clustersListbox = self.windowFormController.clustersListbox
        clustersListbox.delete(0, tkinter.END)
        for i in range(len(clusteringResult.clustersWords)):
            clusterText = ''
            clusterText += '(' + str(clusteringResult.clustersItemsCount[i]) + ')'
            clusterText += ' '
            clusterText += ', '.join(clusteringResult.clustersWords[i])
            clustersListbox.insert(tkinter.END, clusterText)

    # noinspection PyUnusedLocal
    def clustersListboxClick(self, event: tkinter.Event):
        messagesListbox = self.windowFormController.messagesListbox
        openClusterInSublimeButton = self.windowFormController.openClusterInSublimeButton
        messageTextBox = self.windowFormController.messageTextBox
        clustersListbox = self.windowFormController.clustersListbox

        currSelection = clustersListbox.curselection()
        if not len(currSelection):
            return
        selectedCluster = currSelection[0]
        self.selectedCluster = selectedCluster
        cluster = self.clusteringResult.clustersItems[selectedCluster]
        messagesListbox.delete(0, tkinter.END)
        for i in cluster:
            messagesListbox.insert(tkinter.END, self.clusteringResult.texts[i])

    @staticmethod
    def messagesListBoxClick(event: tkinter.Event, messageTextBox: tkinter.Text):
        listbox = event.widget
        currSelection = listbox.curselection()
        if not len(currSelection):
            return
        currText = listbox.get(currSelection, currSelection)[0]
        messageTextBox['state'] = tkinter.NORMAL
        messageTextBox.delete(1.0, tkinter.END)
        messageTextBox.insert(1.0, currText)
        messageTextBox['state'] = tkinter.DISABLED
