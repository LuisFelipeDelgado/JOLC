
class Simbolo:
    def __init__(self, tipo, identificador, fila, columna, valor, posicion, globalV, Heap,tipoS=''):
        self.id = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = tipo
        self.valor = valor
        self.posicion = posicion
        self.globalV = globalV
        self.inHeap = Heap
        self.tipoS = tipoS

    def getID(self):
        return self.id

    def setID(self, id):
        self.id = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo  

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getFila(self):
        return self.fila
    
    def getColumna(self):
        return self.columna