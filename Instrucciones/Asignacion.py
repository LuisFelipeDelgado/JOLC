from TS.Tipo import TIPOS
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from Abstract.instruccion import Expresion
from TS.Simbolo import Simbolo

class Asignacion(Expresion):
    def __init__(self, identificador, expresion, fila, columna, tipo=None):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = tipo

    def interpretar(self, tree, table):
        if isinstance(self.tipo, Excepcion):
            return self.tipo
        value = None
        if(self.tipo==None):
            value = self.expresion.interpretar(tree, table)
            if isinstance(value, Excepcion):
                return value
        else:
            value = self.expresion.interpretar(tree, table)
            if isinstance(value, Excepcion):
                return value
            if(value.tipo!=self.tipo.tipos):
                return Excepcion("Semantico", "Tipo erroneo para declaracion",self.fila,self.columna)
        simbolo = Simbolo(self.tipo, self.identificador, self.fila, self.columna, value)

        result = table.actualizarTabla(simbolo)     # Si no se encuentra el simbolo, lo agrega 

        if isinstance(result,Excepcion): return result
    
        return None

    def getNodo(self):
        nodo = NodoAST("ASIGNACION")
        nodo2 = NodoAST("IDENTIFICADOR")
        nodo2.agregarHijo(str(self.identificador))
        nodo.agregarHijoNodo(nodo2)
        nodo.agregarHijo("=")
        nodo3 = NodoAST("EXPRESION")
        nodo3.agregarHijoNodo(self.expresion.getNodo())
        nodo.agregarHijoNodo(nodo3)
        if self.tipo is not None:
            nodo.agregarHijo("::")
            nodo2 = NodoAST("TIPO")
            tmp = self.returnTipo()
            nodo2.agregarHijo(tmp)
            nodo.agregarHijoNodo(nodo2)
        nodo.agregarHijo(";")
        return nodo

    def returnTipo(self):
        ret=""
        if self.tipo.tipos==TIPOS.CADENA:
            ret="String"
        elif self.tipo.tipos==TIPOS.BOOLEANO:
            ret="Bool"
        elif self.tipo.tipos==TIPOS.DECIMAL:
            ret="Float64"
        elif self.tipo.tipos==TIPOS.ENTERO:
            ret="Int64"
        elif self.tipo.tipos==TIPOS.ARREGLO:
            ret="Arreglo"
        elif self.tipo.tipos==TIPOS.CHARACTER:
            ret="Char"
        return ret