import tkinter
import os
import subprocess
import sys
from ClusteringResult import ClusteringResult
from WindowFormController import WindowFormController


class WindowFormEventHandler:
    def __init__(self, windowWidth: int, windowHeight: int, clusterTempFile: str, textEditorPath: str):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.clusterTempFile = clusterTempFile
        self.textEditorPath = textEditorPath

    def onWindowChange(self, event: tkinter.Event):
        self.windowWidth = event.width
        self.windowHeight = event.height

    def onWindowClose(self):
        if os.path.exists(self.clusterTempFile):
            os.remove(self.clusterTempFile)
        quit()

    def openInSublime(self, event: tkinter.Event, needQuit=False):
        subprocess.Popen([self.textEditorPath, sys.argv[1]])
        if needQuit:
            quit()

    def openClusterInSublime(self, clusteringResult: ClusteringResult, selectedCluster: int):
        f = open(self.clusterTempFile, 'w')
        for messageId in clusteringResult.clustersItems[selectedCluster]:
            f.write(clusteringResult.texts[messageId])
        f.close()
        subprocess.Popen([self.textEditorPath, self.clusterTempFile])

    def renderResult(self, clusteringResult: ClusteringResult, windowFormController: WindowFormController):
        clustersListbox = windowFormController.clustersListbox
        clustersListbox.delete(0, tkinter.END)
        clustersListbox.bind('<<ListboxSelect>>', lambda event: self.clustersListboxClick(event, clusteringResult, windowFormController))
        for i in range(len(clusteringResult.clustersWords)):
            clusterText = ''
            clusterText += '(' + str(clusteringResult.clustersItemsCount[i]) + ')'
            clusterText += ' '
            clusterText += ', '.join(clusteringResult.clustersWords[i])
            clustersListbox.insert(tkinter.END, clusterText)

    def clustersListboxClick(self, event: tkinter.Event, clusteringResult: ClusteringResult, windowFormController: WindowFormController):
        messagesListbox = windowFormController.messagesListbox
        openClusterInSublimeButton = windowFormController.openClusterInSublimeButton
        messageTextBox = windowFormController.messageTextBox

        listbox = event.widget
        currSelection = listbox.curselection()
        if not len(currSelection):
            return
        selectedCluster = currSelection[0]
        cluster = clusteringResult.clustersItems[selectedCluster]
        messagesListbox.delete(0, tkinter.END)
        messagesListbox.bind('<<ListboxSelect>>', lambda listboxEvent: self.messagesListBoxClick(listboxEvent, messageTextBox))
        openClusterInSublimeButton.bind("<Button-1>", lambda buttonEvent: self.openClusterInSublime(clusteringResult, selectedCluster))
        for i in cluster:
            messagesListbox.insert(tkinter.END, clusteringResult.texts[i])

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
