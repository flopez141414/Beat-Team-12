import r2pipe
import json

# opens binary file and extracts variables, strings, imports, functions, packet info, and struct info
from PyQt5.QtWidgets import QFileDialog

rlocal = r2pipe.open("/bin/ping")
#     global variableInfo = rlocal.cmd()
stringInfo = rlocal.cmd('izzj')
dllInfo = rlocal.cmd('iij')
functionInfo = rlocal.cmd('aaa ; aflj')
binaryInfo = rlocal.cmd('iI').splitlines()
#     global packetInfo = rlocal.cmd('afl')
#     global structInfo = rlocal.cmd('afl')

def parseStrings(r2str):
    myr2str = json.loads(r2str)
    mystuff = []
#     print(myr2str['strings'][0]['string'])
    for key in myr2str['strings']:
#         print(key['string'])
        mystuff.append(key['string'])
        
    #for finding duplicate strings    
    mystuff.sort()
    for i in range(len(mystuff)-1):
        if mystuff[i] == mystuff[i+1]:
            print('FOUND ONE', mystuff[i])
#     print(mystuff)

def parseDll(r2dll):
    print(r2dll)
    
def parseFunction(r2func):
    print(r2func)
    
def parseBinaryInfo(r2binfo):
#     for i in r2binfo:
    print(type(r2binfo[0]))
    
    
# parseStrings(stringInfo)
parseBinaryInfo(binaryInfo)

#method to open file explorer
def OpenFile(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                              "All Files (*);;Python Files (*.py)", options=options)
    if fileName:
        print(fileName)
        return fileName

    return "not found"