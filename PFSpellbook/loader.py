




from abc import ABC, abstractmethod
from typing import Any


class AnyLoader(ABC):

    def __init__(self, sourcefile: str):
        self._src = sourcefile
    
    @staticmethod
    def getLoader(sourcefile: str):
        if sourcefile == "5footstep.ini":
            return FIVEFOOTSTEP(sourcefile)
        elif sourcefile == "aon.ini":
            return AON(sourcefile)
        elif sourcefile == "d20pfsrd.ini":
            return D20PFSRD(sourcefile)
        else:
            raise TypeError("Invalid ini file: "+sourcefile+" is not recognised!")
        pass    
    
    @abstractmethod
    def loadFromSource() -> dict:
        pass
        
        
class D20PFSRD(AnyLoader):
    
    def __init__(self, sourcefile: str):
        super().__init__(sourcefile)
        
        
class AON(AnyLoader):
    
    def __init__(self, sourcefile: str):
        super().__init__(sourcefile)
        
class FIVEFOOTSTEP(AnyLoader):
    
    def __init__(self, sourcefile: str):
        super().__init__(sourcefile)