import sys
import winreg

class FilePathController:
    @staticmethod
    def getScriptFolder():
        currentScriptPath = sys.argv[0]
        currentScriptPath = currentScriptPath.replace('/', '\\')
        lastSlashPos = currentScriptPath.rfind('\\')
        currentScriptFolder = currentScriptPath[:lastSlashPos]

        return currentScriptFolder

    @staticmethod
    def getLogPath():
        logPath = sys.argv[1] if len(sys.argv) > 1 else ''

        return logPath

    @staticmethod
    def getClusterTempFilePath():
        tempFolderKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment')
        tempFolder = winreg.QueryValueEx(tempFolderKey, 'TEMP')
        tempFolderKey.Close()
        tempFolder = tempFolder[0]
        tempFolder = winreg.ExpandEnvironmentStrings(tempFolder)
        clusterTempFile = tempFolder + r'\log-cluster.txt'

        return clusterTempFile
