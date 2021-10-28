from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Expresion
from TS.Tipo import TIPOS

class Parametro(Expresion):

    def __init__(self, id, tipo, fila, columna):
        self.tipos=None
        if isinstance(tipo,list):
            Expresion.__init__(self, TIPOS.ARREGLO,fila, columna)
            self.tipos=tipo
        else:
            Expresion.__init__(self, tipo,fila, columna)
        self.nombre = id
    
    def interpretar(self, table,tree):
        return self

    def getNodo(self):
        nodo = NodoAST("RETURN")
        nodo.agregarHijo("return")
        if self.expresion!= None:
            nodo.agregarHijoNodo(self.expresion.getNodo())
        nodo.agregarHijo(";")
        return nodo