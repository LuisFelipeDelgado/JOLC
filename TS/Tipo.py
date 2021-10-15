from enum import Enum

class TIPO():
    def __init__(self, tipos):
        self.tipos = tipos

    def getTipos(self):
        return self.tipos

    def setTipos(self, tipos):
        self.tipos = tipos

class TIPOS(Enum):
    ENTERO = 1
    DECIMAL = 2
    CHARACTER = 3
    BOOLEANO = 4
    CADENA = 5
    NULO = 6
    ARREGLO = 7
    FUNCION = 8
    STRUCT = 9
