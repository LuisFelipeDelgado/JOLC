import copy
from TS.Simbolo import Simbolo
from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPOS
from Instrucciones.Return import ReturnI
from Excepciones.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class Struct(Expresion):
    def __init__(self, nombre, atributos, fila, columna, mutable=None):
        self.nombre = nombre
        self.atributos = atributos
        self.fila = fila
        self.columna = columna
        self.mutable = mutable
    
    def interpretar(self, tree, table):
        dictdec={'mutable':False}
        if self.mutable:
            dictdec['mutable']=True
        dictdec['atributos']=copy.deepcopy(self.atributos)
        declara = Simbolo(TIPOS.STRUCT, self.nombre, self.fila, self.columna, copy.deepcopy(dictdec))
        result = table.actualizarTabla(declara)
        return None

    def getNodo(self):
        nodo1 = NodoAST("DECLARAR STRUCT")
        if self.mutable:
            nodo1.agregarHijo("mutable")
        nodo1.agregarHijo("struct")
        nodo1.agregarHijo(str(self.nombre))
        nodo = NodoAST("ATRIBUTOS")
        bs = True
        for i in self.atributos:
            if bs:
                instruccioness3 = NodoAST("ATRIBUTO")
                instruccioness3.agregarHijo(i)
                instruccioness3.agregarHijo(";")
                nodo.agregarHijoNodo(instruccioness3)
                bs=False
            else:
                instrtmp = nodo
                instruccioness3 = NodoAST("ATRIBUTO")
                nodo = NodoAST("ATRIBUTOS")
                nodo.agregarHijoNodo(instrtmp)
                instruccioness3.agregarHijo(i)
                instruccioness3.agregarHijo(";")
                nodo.agregarHijoNodo(instruccioness3)
        nodo1.agregarHijoNodo(nodo)
        nodo1.agregarHijo("end")
        nodo1.agregarHijo(";")
        return nodo1