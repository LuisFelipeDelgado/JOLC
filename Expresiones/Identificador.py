from Abstract.instruccion import Expresion
from Excepciones.Excepcion import Excepcion
from Abstract.NodoAST import NodoAST


class Identificador(Expresion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        simbolo = table.getVariable(self.identificador)

        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        
        return simbolo.getValor()

    def getNodo(self):
        nodo = NodoAST("IDENTIFICADOR")
        nodo.agregarHijo(str(self.identificador))
        return nodo