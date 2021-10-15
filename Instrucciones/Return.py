from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from TS.Tipo import TIPOS
from TS.TablaSimbolos import TablaSimbolos

class Return(Expresion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        result=None
        if self.expresion!=None:
            result = self.expresion.interpretar(tree, table)
        if isinstance(result, Excepcion): return result
        self.result = result            #VALOR DEL RESULT
        return self

    def getNodo(self):
        nodo = NodoAST("RETURN")
        nodo.agregarHijo("return")
        if self.expresion!= None:
            nodo.agregarHijoNodo(self.expresion.getNodo())
        nodo.agregarHijo(";")
        return nodo