from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from TS.TCI import TCI

class Break(Expresion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        if table.breakE == '':
            return
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        codigoR.GoTo(table.breakE)

    def getNodo(self):
        nodo = NodoAST("BREAK")
        nodo.agregarHijo("break")
        nodo.agregarHijo(";")
        return nodo