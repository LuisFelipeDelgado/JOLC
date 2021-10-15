from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST

class Continue(Expresion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoAST("CONTINUE")
        nodo.agregarHijo("continue")
        nodo.agregarHijo(";")
        return nodo