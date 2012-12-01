from configmanager import cmapi

def getMaxItemHash4Cache():
    return cmapi.getItemValue('maxitemhash', 1000)

