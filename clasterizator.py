import sys
import tkinter
from tkinter import *

import pandas

from ClusteringResult import ClusteringResult

import numpy

from ClusteringObject import ClusteringObject
import string
import subprocess
import os


def openInSublime():
    subprocess.Popen([r'C:\Program Files\Sublime Text\sublime_text.exe', sys.argv[1]])
    # quit()


def startClustering(logPath):
    startRowRegExp = str(regExpEntry.get())
    clusteringResult = ClusteringObject().main(logPath, startRowRegExp, window)
    # clusteringResult.printSelf()
    renderResult(clusteringResult)


# if len(sys.argv) > 1:
#     openInSublime()

'''
Подстановочные шаблоны:
!! становится восклицательным знаком
!/ становится текущим путём на стороне удалённого сервера
!@ становится именем хоста для текущей сессии
!U становится именем пользователя для текущей сессии
!Р становится паролем для текущей сессии
!# становится номером порта для текущей сессии
!N становится именем текущей сессии
!?prompt[\]?default! становится заданным пользователем значением с заданным приглашением(prompt)
и значением по-умолчанию(default) (опционально \ для избежания escape-преобразования)
!`command` становится выводом результата выполнения локальной комманды(command))
'''
# python "C:\Users\borodin_admin\Desktop\Институт\_ВКР\2022-06-14 Приложение\winscp-integration\clasterizator.py"
# python "C:\Users\borodin_admin\Desktop\Институт\_ВКР\2022-06-14 Приложение\winscp-integration\clasterizator.py" !.! !/ !@ !U !N

window = Tk()
window.title("Кластеризатор сообщений журнальных файлов")
# window.geometry('900x200')
window.minsize(700, 600)
window.iconbitmap(r'C:\borodin_admin\Институт\_ВКР\2022-06-14 Приложение\winscp-integration\icon.ico')

windowWidth = 700
windowHeight = 600


def onWindowChange(event: tkinter.Event):
    windowWidth = event.width
    windowHeight = event.height

def onWindowClose():
    if os.path.exists(clusterTempFile):
        os.remove(clusterTempFile)
    quit()


window.bind("<Configure>", onWindowChange)
window.protocol("WM_DELETE_WINDOW", onWindowClose)

logPath = sys.argv[1] if len(sys.argv) > 1 else ''

print(logPath)

topContainer = LabelFrame(window, bd=3, height=50, text='Журнальный файл')
topContainer.pack(expand=False, fill=BOTH, pady=5, padx=5)
logPathLabel = tkinter.Label(topContainer, text=logPath, anchor='w')
logPathLabel.place(height=26, y=13, x=3, relwidth=0.68, anchor='w')
openInSublimeButton = Button(topContainer, text="Открыть весь лог в SublimeText", command=openInSublime)
openInSublimeButton.place(height=29, relwidth=0.29, y=12, relx=0.7, anchor='w')

startRowRegExp = tkinter.StringVar()
startRowRegExp.set(r'(\d{4}-\d{2}-\d{2} {1,2}\d{1,2}:\d{2}:\d{2})')
regExpContainer = LabelFrame(window, text='Определитель начала строк', bd=3, height=50)
regExpContainer.pack(expand=False, fill=BOTH, pady=5, padx=5)
regExpLabel = tkinter.Label(regExpContainer, text='RegExp для начала строк:', anchor='e')
regExpLabel.place(height=26, y=13, x=3, relwidth=0.23, anchor='w')
regExpEntry = tkinter.Entry(regExpContainer, textvariable=startRowRegExp)
regExpEntry.place(height=26, y=13, relx=0.25, relwidth=0.53, anchor='w')
startClusteringButton = Button(regExpContainer, text="Кластеризовать", command=lambda: startClustering(logPath))
startClusteringButton.place(height=29, relwidth=0.19, y=12, relx=0.8, anchor='w')

# if False:
#     searchString = tkinter.StringVar()
#     searchString.set('Строка поиска')
#     searchContainer = LabelFrame(window, text='Поиск', bd=3, height=50)
#     searchContainer.pack(side=BOTTOM, expand=False, fill=BOTH, pady=5, padx=5)
#     searchEntry = tkinter.Entry(searchContainer, textvariable=searchString)
#     searchEntry.place(height=26, y=13, x=3, relwidth=0.78, anchor='w')
#     searchButton = Button(searchContainer, text="Найти")
#     searchButton.place(height=29, relwidth=0.19, y=12, relx=0.8, anchor='w')

clusteringResultGlobal = None

import winreg
tempFolderKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment')
tempFolder = winreg.QueryValueEx(tempFolderKey, 'TEMP')
tempFolderKey.Close()
tempFolder = tempFolder[0]
tempFolder = winreg.ExpandEnvironmentStrings(tempFolder)
clusterTempFile = tempFolder + r'\log-cluster.txt'

settingsFile = open('settings.json', 'w')
settingsFile.close()

def clustersListboxClick(event: tkinter.Event, clusteringResult: ClusteringResult):
    listbox = event.widget
    currSelection = listbox.curselection()
    if not len(currSelection):
        return
    selectedCluster = currSelection[0]
    cluster = clusteringResult.clustersItems[selectedCluster]
    messagesListbox.delete(0, tkinter.END)
    messagesListbox.bind('<<ListboxSelect>>', lambda event: messagesListBoxClick(event, clusteringResult))
    openClusterInSublimeButton.bind("<Button-1>", lambda event: openClusterInSublime(clusteringResult, selectedCluster))
    for i in cluster:
        messagesListbox.insert(END, clusteringResult.texts[i])

def openClusterInSublime(clusteringResult: ClusteringResult, selectedCluster: int):
    f = open(clusterTempFile, 'w')
    for messageId in clusteringResult.clustersItems[selectedCluster]:
        f.write(clusteringResult.texts[messageId])
    f.close()
    subprocess.Popen([r'C:\Program Files\Sublime Text\sublime_text.exe', clusterTempFile])


def messagesListBoxClick(event: tkinter.Event, clusteringResult: ClusteringResult):
    listbox = event.widget
    currSelection = listbox.curselection()
    if not len(currSelection):
        return
    currText = listbox.get(currSelection, currSelection)[0]
    messageTextBox['state'] = NORMAL
    messageTextBox.delete(1.0, END)
    messageTextBox.insert(1.0, currText)
    messageTextBox['state'] = DISABLED

bodyContainer = Frame(window)
bodyContainer.pack(pady=5, padx=5, fill=BOTH, expand=True)
clustersListContainer = LabelFrame(bodyContainer, text='Clusters', bd=3, padx=5, pady=5)
clustersListContainer.place(relheight=1, x=3, relwidth=0.28, rely=0.5, anchor='w')
clustersListbox = tkinter.Listbox(clustersListContainer)
clustersListbox.place(relheight=1, relx=0, rely=0.5, relwidth=1, anchor='w')

messagesContainer = LabelFrame(bodyContainer, text='Сообщения', bd=3, padx=5, pady=5)
messagesContainer.place(relheight=1, relx=0.3, relwidth=0.68, rely=0.5, anchor='w')

openClusterInSublimeButton = tkinter.Button(messagesContainer, text='Открыть кластер в SublimeText')
openClusterInSublimeButton.place(relx=1, width=200, rely=0, anchor='ne')
# openClusterInSublimeButton.pack()

messagesListbox = Listbox(messagesContainer)
messagesListbox.place(relx=0, relwidth=1, rely=0.08, relheight=0.45, anchor='nw')
# messagesListbox.pack(fill=X, pady=5)


messageTextBox = tkinter.Text(messagesContainer, wrap=WORD, state=DISABLED)
messageTextBox.place(relx=0, relwidth=1, rely=0.56, relheight=0.43, anchor='nw')


# messageTextBox.pack(fill=X)


# contextUpButton = tkinter.Button(messagesContainer, text='Вверх')
# contextUpButton.pack(fill=X)
# contextContainer = tkinter.Frame(messagesContainer)
# prevMessageLabel = tkinter.Label(contextContainer, text='Предыдущее сообщение', anchor='w')
# prevMessageLabel.pack(fill=X)
# currentMessageLabel = tkinter.Label(contextContainer, text='Текущее сообщение', anchor='w')
# currentMessageLabel.pack(fill=BOTH)
# nextMessageLabel = tkinter.Label(contextContainer, text='Следующее сообщение', anchor='w')
# nextMessageLabel.pack(fill=X)
# contextContainer.pack(fill=BOTH)
# contextDownButton = tkinter.Button(messagesContainer, text='Вниз')
# contextDownButton.pack(fill=X)

def renderResult(clusteringResult: ClusteringResult):
    print('')
    # print(clusteringResult.clustersWords)
    # print(clusteringResult.clustersItemsCount)
    clustersListbox.delete(0, tkinter.END)
    clustersListbox.bind('<<ListboxSelect>>', lambda event: clustersListboxClick(event, clusteringResult))
    for i in range(len(clusteringResult.clustersWords)):
        clusterText = ''
        clusterText += '(' + str(clusteringResult.clustersItemsCount[i]) + ')'
        clusterText += ' '
        clusterText += ', '.join(clusteringResult.clustersWords[i])
        clustersListbox.insert(END, clusterText)


# container = Frame(window)
# container.pack(side='left', anchor='n')
#
# labels = []
# rowNum = 0
# for parameter in sys.argv:
#     label = tkinter.Label(container, text=parameter, justify='left')
#     label.grid(row=rowNum, column=0, padx="5", pady="5", sticky='w')
#     rowNum += 1

# if len(sys.argv) > 1:
#     openInSublimeButton = Button(window, text="Открыть в SublimeText", command=openInSublime)
#     openInSublimeButton.pack(side='right', padx="10", pady='5', anchor='n')
#
#     logPath = sys.argv[1]
#     startRowRegExp = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
#
#     startClusteringButton = Button(window, text="Кластеризовать", command=lambda: startClustering(logPath, startRowRegExp))
#     startClusteringButton.pack(side='right', padx="10", pady='5', anchor='n')
#     # startClusteringButton.bind("<Button-1>", lambda event: startClustering(logPath, startRowRegExp, event))
#
#     window.bind('<<startClusteringEvent>>', lambda event: startClusteringInner(logPath, startRowRegExp))

window.mainloop()
