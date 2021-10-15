import time


class Excepcion():
    def __init__(self, tipo, descripcion, fila, columna):
        self.tipo = tipo
        self.descripcion = descripcion
        self.linea = fila
        self.columna = columna
        self.tiempo = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def toString(self):
        return self.tipo + " - " + self.descripcion + " [" + str(self.linea) + "," + str(self.columna) + "]"

    def imprimir(self):
        return self.toString()

    def getTipo(self):
        return self.tipo

    def getDescripcion(self):
        return self.descripcion

    def getLinea(self):
        return self.linea

    def getColumna(self):
        return self.columna
