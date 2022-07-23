import time


class Profiler:
    def __init__(self):
        self.points = {}
        self.lastTimestamp = time.time_ns()

    def start(self):
        self.lastTimestamp = time.time_ns()
        print('Profiler: ' + 'start')

    def addPoint(self, pointName: str):
        currentTime = time.time_ns()
        durationNs = currentTime - self.lastTimestamp
        durationSec = durationNs / 1000 / 1000 / 1000
        self.points[pointName] = durationSec
        self.lastTimestamp = currentTime
        print('Profiler: ' + pointName + f' ({durationSec:.3f} c)')

    def print(self):
        print('timeProfiler')
        print(self.points)
