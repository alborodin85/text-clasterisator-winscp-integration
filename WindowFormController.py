import tkinter


class WindowFormController:
    def __init__(self, currentScriptFolder: str, windowWidth: int, windowHeight: int, logPath: str, startRowRowRegExpInit: str, startClusteringCallback: callable):
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
        self.messagesListbox = tkinter.Listbox()
        self.messageTextBox = tkinter.Text()
        self.openClusterInSublimeButton = tkinter.Button()

        self.buildTopContainer(logPath)
        self.buildRegExpContainer(startRowRowRegExpInit, lambda: startClusteringCallback(logPath))
        self.buildBodyContainer()
        self.buildSearchContainer()

    def buildTopContainer(self, logPath: str):
        topContainer = tkinter.LabelFrame(self.window, bd=3, height=50, text='Журнальный файл')
        topContainer.pack(expand=False, fill=tkinter.BOTH, pady=5, padx=5)
        logPathLabel = tkinter.Label(topContainer, text=logPath, anchor='w')
        logPathLabel.place(height=26, y=13, x=3, relwidth=0.68, anchor='w')
        openInSublimeButton = tkinter.Button(topContainer, text="Открыть весь лог в SublimeText")
        openInSublimeButton.place(height=29, relwidth=0.29, y=12, relx=0.7, anchor='w')
        self.openInSublimeButton = openInSublimeButton

    def buildRegExpContainer(self, startRowRowRegExpInit: str, startClusterCallback: callable):
        startRowRegExp = tkinter.StringVar()
        startRowRegExp.set(startRowRowRegExpInit)
        regExpContainer = tkinter.LabelFrame(self.window, text='Определитель начала строк', bd=3, height=50)
        regExpContainer.pack(expand=False, fill=tkinter.BOTH, pady=5, padx=5)
        regExpLabel = tkinter.Label(regExpContainer, text='RegExp для начала строк:', anchor='e')
        regExpLabel.place(height=26, y=13, x=3, relwidth=0.23, anchor='w')
        regExpEntry = tkinter.Entry(regExpContainer, textvariable=startRowRegExp)
        regExpEntry.place(height=26, y=13, relx=0.25, relwidth=0.53, anchor='w')
        self.regExpEntry = regExpEntry
        startClusteringButton = tkinter.Button(regExpContainer, text="Кластеризовать", command=startClusterCallback)
        startClusteringButton.place(height=29, relwidth=0.19, y=12, relx=0.8, anchor='w')
        self.startClusteringButton = startClusteringButton

    def buildBodyContainer(self):
        bodyContainer = tkinter.Frame(self.window)
        bodyContainer.pack(pady=5, padx=5, fill=tkinter.BOTH, expand=True)
        clustersListContainer = tkinter.LabelFrame(bodyContainer, text='Clusters', bd=3, padx=5, pady=5)
        clustersListContainer.place(relheight=1, x=3, relwidth=0.28, rely=0.5, anchor='w')
        clustersListbox = tkinter.Listbox(clustersListContainer)
        clustersListbox.place(relheight=1, relx=0, rely=0.5, relwidth=1, anchor='w')
        self.clustersListbox = clustersListbox
        messagesContainer = tkinter.LabelFrame(bodyContainer, text='Сообщения', bd=3, padx=5, pady=5)
        messagesContainer.place(relheight=1, relx=0.3, relwidth=0.68, rely=0.5, anchor='w')
        openClusterInSublimeButton = tkinter.Button(messagesContainer, text='Открыть кластер в SublimeText')
        openClusterInSublimeButton.place(relx=1, width=200, rely=0, anchor='ne')
        self.openClusterInSublimeButton = openClusterInSublimeButton
        messagesListbox = tkinter.Listbox(messagesContainer)
        messagesListbox.place(relx=0, relwidth=1, rely=0.08, relheight=0.45, anchor='nw')
        self.messagesListbox = messagesListbox
        messageTextBox = tkinter.Text(messagesContainer, wrap=tkinter.WORD, state=tkinter.DISABLED)
        messageTextBox.place(relx=0, relwidth=1, rely=0.56, relheight=0.43, anchor='nw')
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
