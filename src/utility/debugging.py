import os
import inspect

def _scriptName(stackDepth):
    return inspect.getfile(inspect.currentframe(stackDepth))

def currentFile(stackDepth=1):
    scriptName = _scriptName(stackDepth)
    scriptDirectory = currentDirectory(scriptName)

    return os.path.join(scriptDirectory,scriptName)
    
def currentDirectory(scriptName=None,stackDepth=1):
    if not scriptName:
        scriptName = _scriptName(stackDepth)
    return os.path.dirname(os.path.abspath(scriptName))
    

if __name__ == '__main__':
    print currentFile(0)