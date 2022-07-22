class SettingsController:
    def __init__(self, currentScriptFolder: str):
        settingsFileName = currentScriptFolder + r'\settings.json'
        settingsFile = open(settingsFileName, 'w')
        settingsFile.close()
