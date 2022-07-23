import os
import pandas
import re


class DataRetriever:
    @staticmethod
    def readFile(logPath: str) -> str:
        fileSize = os.path.getsize(logPath)
        logFile = open(logPath, 'rb')
        textFile = ''
        chunkSize = fileSize // 10
        msg = logFile.read(chunkSize)
        lineNumber = 0
        while len(msg):
            lineNumber += 1
            textFile += str(msg)
            msg = logFile.read(chunkSize)

        logFile.close()

        textFile = textFile.replace(r'\n', '\n')
        textFile = textFile.replace(r'\t', '\t')

        return textFile

    @staticmethod
    def splitText(startRowRegExp: str, textFile: str, countRows: int) -> pandas.Series:
        logRecordsList = re.split(startRowRegExp, textFile, flags=re.MULTILINE)
        countRows = countRows if countRows else None
        textsRaw = logRecordsList[:countRows]
        texts = []
        for i in range(1, len(textsRaw), 2):
            if i + 1 < len(textsRaw):
                texts.append(textsRaw[i] + ' ' + textsRaw[i + 1])

        texts = pandas.Series(texts)

        return texts
