import os  # for SimpleNamer
import inspect  # for SimpleNamer
import sys
from configparser import ConfigParser

import subprocess


def common_overlap(predecessor, successor):
    for index in range(len(predecessor)):
        reverse_index = -(index + 1)
        subset = predecessor[reverse_index:]
        front = successor[:-reverse_index]
        if subset == front:
            return subset
    return []


class SimpleNamer():
    def __init__(self, testcase):
        testcase_id = testcase.id()
        source_file_path = os.path.dirname(inspect.getfile(testcase.__class__))

        successor = testcase_id.split('.')
        predecessor = source_file_path.split('\\')
        common = common_overlap(predecessor, successor)
        successor = successor[len(common):]

        self.test_case_name = '_'.join(successor)
        self.source_file_path = source_file_path


class TextFileApprover():
    def __init__(self, data, namer):
        bounds = '--\n'
        self.actual = bounds + str(data) + '\n' + bounds
        self.namer = namer
        self.findTortoiseMerge()

    def findTortoiseMerge(self):
        self.tortoiseMerge = r'C:\Program Files\TortoiseSVN\bin\TortoiseMerge.exe'
        config = ConfigParser()
        config.read('ApprovalsTests.ini')
        try:
            self.tortoiseMerge = config['TortoiseMerge'].get('FullPath', raw=True, fallback=self.tortoiseMerge)
        except KeyError:
            pass

    def extensionName(self):
        return 'txt'

    def approvedName(self):
        return '.approved'

    def receivedName(self):
        return '.received'

    def makeFilenameWith(self, insert):
        return os.path.join(self.namer.source_file_path,
                            '_' + self.namer.test_case_name + insert + os.path.extsep + self.extensionName())

    def approvedFilename(self):
        return self.makeFilenameWith(self.approvedName())

    def receivedFileName(self):
        return self.makeFilenameWith(self.receivedName())

    def readFileMode(self):
        return 'r'

    def writeFileMode(self):
        return 'w'

    def approved_exists(self):
        try:
            fname = self.approvedFilename()
            with open(fname, self.readFileMode()) as f:
                self.approved = f.read()
                return True
        except IOError:
            pass
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return False

    def fail(self, testcase):
        testcase.fail(self.namer.test_case_name)

    def writeReceived(self):
        with open(self.receivedFileName(), self.writeFileMode()) as f:
            f.write(self.actual)

    def removeReceived(self):
        try:
            os.remove(self.receivedFileName())
        except IOError:
            pass

    def diffProgram(self):
        return self.tortoiseMerge

    def startDiff(self, receivedFileName, approvedFilename):
        fmt = '{0}'
        rFile = fmt.format(receivedFileName)
        aFile = fmt.format(approvedFilename)
        subprocess.call([self.diffProgram(), rFile, aFile])

    def createEmpty(self, fileName):
        open(fileName, 'a')

    def touchApproved(self):
        if not self.approved_exists():
            self.createEmpty(self.approvedFilename())

    def report(self):
        self.touchApproved()
        self.startDiff(self.receivedFileName(), self.approvedFilename())

    def actualAndApprovedMatch(self):
        if self.approved_exists():
            if self.actual == self.approved:
                self.removeReceived()
                return True
        return False


def GetApprover(data, testcase):
    namer = SimpleNamer(testcase)
    return TextFileApprover(data, namer)


class Approvals():
    def verify(self, testcase, data):
        approver = GetApprover(data, testcase)
        if approver.actualAndApprovedMatch():
            return True
        approver.writeReceived()
        approver.report()  # Block with a GUI so that user can fiddle with files
        if approver.actualAndApprovedMatch():
            return True
        approver.fail(testcase)
