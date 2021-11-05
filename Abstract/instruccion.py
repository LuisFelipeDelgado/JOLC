from abc import ABC, abstractmethod

class Expresion(ABC):
    def __init__(self, tipo, fila, columna):
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.ev = ''
        self.ef = ''
        self.tipoS = ''
        super().__init__()

    @abstractmethod
    def interpretar(self,tree, table):
        pass

    @abstractmethod
    def getNodo(self):
        pass
