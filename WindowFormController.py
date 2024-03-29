import tkinter


class WindowFormController:
    def __init__(
            self,
            currentScriptFolder: str,
            windowWidth: int,
            windowHeight: int,
            logPath: str,
            startRowRegExpInit: str,
            textEditorPathInit: str,
            algorithmIdValueInit: int,
            countClustersValueInit: int,
            countRowsValueInit: int,
    ):
        window = tkinter.Tk()
        window.title("Кластеризатор сообщений журнальных файлов")
        window.minsize(windowWidth, windowHeight)
        window.iconbitmap(currentScriptFolder + r'\icon.ico')
        self.window = window
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.openInSublimeButton = tkinter.Button()
        self.startClusteringButton = tkinter.Button()
        self.regExpEntry = tkinter.Entry()
        self.clustersListbox = tkinter.Listbox()
        self.clusterTextBox = tkinter.Text()
        self.messagesListbox = tkinter.Listbox()
        self.messageTextBox = tkinter.Text()
        self.openClusterInSublimeButton = tkinter.Button()
        self.textEditorEntry = tkinter.Entry()
        self.saveTextEditorButton = tkinter.Button()
        self.clustersListContainer = tkinter.LabelFrame()
        self.settingsButton = tkinter.Button()

        self.algorithmId = tkinter.IntVar()
        self.algorithmId.set(algorithmIdValueInit)
        self.countClusters = tkinter.StringVar()
        self.countClusters.set(str(countClustersValueInit))
        self.countRows = tkinter.StringVar()
        self.countRows.set(str(countRowsValueInit))

        self.buildTextEditorContainer(textEditorPathInit)
        self.buildTopContainer(logPath)
        self.buildRegExpContainer(startRowRegExpInit)
        self.buildAlgorithmContainer()
        self.buildBodyContainer()

    def buildTextEditorContainer(self, textEditorPathInit: str):
        textEditorPath = tkinter.StringVar()
        textEditorPath.set(textEditorPathInit)
        textEditorContainer = tkinter.LabelFrame(self.window, text='Текстовый редактор', bd=3, height=50)
        textEditorContainer.pack(expand=False, fill=tkinter.BOTH, pady=5, padx=5)
        textEditorLabel = tkinter.Label(textEditorContainer, text='Путь к текст. редактору:', anchor='e')
        textEditorLabel.place(height=26, y=13, x=3, relwidth=0.23, anchor='w')
        textEditorEntry = tkinter.Entry(textEditorContainer, textvariable=textEditorPath)
        textEditorEntry.place(height=26, y=13, relx=0.25, relwidth=0.48, anchor='w')
        self.textEditorEntry = textEditorEntry
        saveTextEditorButton = tkinter.Button(textEditorContainer, text="Проверить и сохранить")
        saveTextEditorButton.place(height=29, relwidth=0.24, y=12, relx=0.75, anchor='w')
        self.saveTextEditorButton = saveTextEditorButton

    def buildTopContainer(self, logPath: str):
        topContainer = tkinter.LabelFrame(self.window, bd=3, height=50, text='Журнальный файл')
        topContainer.pack(expand=False, fill=tkinter.BOTH, pady=5, padx=5)
        logPathLabel = tkinter.Label(topContainer, text=logPath, anchor='w')
        logPathLabel.place(height=26, y=13, x=3, relwidth=0.68, anchor='w')
        openInSublimeButton = tkinter.Button(topContainer, text="Открыть весь лог в редакторе")
        openInSublimeButton.place(height=29, relwidth=0.29, y=12, relx=0.7, anchor='w')
        self.openInSublimeButton = openInSublimeButton

    def buildRegExpContainer(self, startRowRegExpInit: str):
        startRowRegExp = tkinter.StringVar()
        startRowRegExp.set(startRowRegExpInit)
        regExpContainer = tkinter.LabelFrame(self.window, text='Определитель начала сообщений', bd=3, height=50)
        regExpContainer.pack(expand=False, fill=tkinter.BOTH, pady=5, padx=5)
        regExpLabel = tkinter.Label(regExpContainer, text='RegExp для начала сообщения:', anchor='e')
        regExpLabel.place(height=26, y=13, x=3, relwidth=0.23, anchor='w')
        regExpEntry = tkinter.Entry(regExpContainer, textvariable=startRowRegExp)
        regExpEntry.place(height=26, y=13, relx=0.25, relwidth=0.43, anchor='w')
        self.regExpEntry = regExpEntry

        startClusteringButton = tkinter.Button(regExpContainer, text="Кластеризовать")
        startClusteringButton.place(height=29, relwidth=0.14, y=12, relx=0.7, anchor='w')
        self.startClusteringButton = startClusteringButton

        settingsButton = tkinter.Button(regExpContainer, text="settings.json")
        settingsButton.place(height=29, relwidth=0.14, y=12, relx=0.85, anchor='w')
        self.settingsButton = settingsButton

    def buildAlgorithmContainer(self):
        algorithmContainer = tkinter.LabelFrame(self.window, text='Настройки алгоритма', bd=3, height=50)
        algorithmContainer.pack(expand=False, fill=tkinter.BOTH, pady=5, padx=5)

        dbscanRadio = tkinter.Radiobutton(master=algorithmContainer, text='DBSCAN', value=1, variable=self.algorithmId, padx=15)
        dbscanRadio.pack(side=tkinter.LEFT)
        birchRadio = tkinter.Radiobutton(master=algorithmContainer, text='BIRCH', value=2, variable=self.algorithmId, padx=15)
        birchRadio.pack(side=tkinter.LEFT)
        kmeansRadio = tkinter.Radiobutton(master=algorithmContainer, text='K-MEANS', value=3, variable=self.algorithmId, padx=15)
        kmeansRadio.pack(side=tkinter.LEFT)

        countClusterLabel = tkinter.Label(master=algorithmContainer, text='Число кластеров (для K-MEANS):')
        countClusterLabel.pack(side=tkinter.LEFT)
        countClusterEntry = tkinter.Entry(master=algorithmContainer, textvariable=self.countClusters, width=3)
        countClusterEntry.pack(side=tkinter.LEFT)

        breakLabel = tkinter.Label(master=algorithmContainer, padx=8)
        breakLabel.pack(side=tkinter.LEFT)
        countRowsLabel = tkinter.Label(master=algorithmContainer, text='Оставить строк:')
        countRowsLabel.pack(side=tkinter.LEFT)
        countRowsEntry = tkinter.Entry(master=algorithmContainer, textvariable=self.countRows, width=3)
        countRowsEntry.pack(side=tkinter.LEFT)

    # noinspection DuplicatedCode
    def buildBodyContainer(self):
        bodyContainer = tkinter.Frame(self.window)
        bodyContainer.pack(pady=5, padx=5, fill=tkinter.BOTH, expand=True)

        clustersListContainer = tkinter.LabelFrame(bodyContainer, bd=3, padx=5, pady=5)
        clustersListContainer['text'] = '----------'
        clustersListContainer.place(relheight=0.74, x=3, relwidth=0.33, rely=0.37, anchor='w')
        self.clustersListContainer = clustersListContainer
        clusterScrollBar = tkinter.Scrollbar(clustersListContainer)
        clusterScrollBar.pack(fill=tkinter.Y, side=tkinter.RIGHT)
        clustersListbox = tkinter.Listbox(clustersListContainer, yscrollcommand=clusterScrollBar.set)
        clusterScrollBar.config(command=clustersListbox.yview)
        clustersListbox.pack(fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)
        self.clustersListbox = clustersListbox

        clusterTextBoxContainer = tkinter.Frame(bodyContainer, bd=3, padx=5, pady=5)
        clusterTextBoxContainer.place(relheight=0.25, x=3, relwidth=0.33, rely=0.865, anchor='w')
        clusterTextBoxScrollBar = tkinter.Scrollbar(clusterTextBoxContainer)
        clusterTextBoxScrollBar.pack(fill=tkinter.Y, side=tkinter.RIGHT)
        clusterTextBox = tkinter.Text(clusterTextBoxContainer, wrap=tkinter.WORD, state=tkinter.DISABLED, yscrollcommand=clusterTextBoxScrollBar.set)
        clusterTextBoxScrollBar.config(command=clusterTextBox.yview)
        clusterTextBox.pack(fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)
        self.clusterTextBox = clusterTextBox

        messagesContainer = tkinter.LabelFrame(bodyContainer, text='Сообщения', bd=3, padx=5, pady=5)
        messagesContainer.place(relheight=1, relx=0.35, relwidth=0.63, rely=0.5, anchor='w')
        openClusterInSublimeButton = tkinter.Button(messagesContainer, text='Открыть кластер в редакторе')
        openClusterInSublimeButton.place(relx=1, width=200, rely=0, anchor='ne')
        self.openClusterInSublimeButton = openClusterInSublimeButton

        messagesListboxContainer = tkinter.Frame(messagesContainer)
        messagesListboxContainer.place(relx=0, relwidth=1, rely=0.08, relheight=0.45, anchor='nw')
        messagesListBoxScrollBar = tkinter.Scrollbar(messagesListboxContainer)
        messagesListBoxScrollBar.pack(fill=tkinter.Y, side=tkinter.RIGHT)
        messagesListbox = tkinter.Listbox(messagesListboxContainer, yscrollcommand=messagesListBoxScrollBar.set)
        messagesListBoxScrollBar.config(command=messagesListbox.yview)
        messagesListbox.pack(fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)
        self.messagesListbox = messagesListbox

        messageTextBoxContainer = tkinter.Frame(messagesContainer)
        messageTextBoxContainer.place(relx=0, relwidth=1, rely=0.56, relheight=0.43, anchor='nw')
        messageTextBoxScrollBar = tkinter.Scrollbar(messageTextBoxContainer)
        messageTextBoxScrollBar.pack(fill=tkinter.Y, side=tkinter.RIGHT)
        messageTextBox = tkinter.Text(messageTextBoxContainer, wrap=tkinter.WORD, state=tkinter.DISABLED, yscrollcommand=messageTextBoxScrollBar.set)
        messageTextBoxScrollBar.config(command=messageTextBox.yview)
        messageTextBox.pack(fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)
        self.messageTextBox = messageTextBox

    def buildSearchContainer(self):
        searchString = tkinter.StringVar()
        searchString.set('Строка поиска')
        searchContainer = tkinter.LabelFrame(self.window, text='Поиск', bd=3, height=50)
        searchContainer.pack(side=tkinter.BOTTOM, expand=False, fill=tkinter.BOTH, pady=5, padx=5)
        searchEntry = tkinter.Entry(searchContainer, textvariable=searchString)
        searchEntry.place(height=26, y=13, x=3, relwidth=0.78, anchor='w')
        searchButton = tkinter.Button(searchContainer, text="Найти")
        searchButton.place(height=29, relwidth=0.19, y=12, relx=0.8, anchor='w')
