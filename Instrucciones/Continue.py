from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from TS.TCI import TCI

class Continue(Expresion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        if table.continueE is '':
            return
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        codigoR.GoTo(table.continueE)

    def getNodo(self):
        nodo = NodoAST("CONTINUE")
        nodo.agregarHijo("continue")
        nodo.agregarHijo(";")
        return nodo