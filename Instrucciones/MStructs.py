from copy import copy
from TS.Simbolo import Simbolo
from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPOS
from Instrucciones.Return import Return
from Excepciones.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class MStruct(Expresion):
    def __init__(self, nombre, atributos, expresion, fila, columna):
        self.nombre = nombre
        self.atributos = atributos
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        nuevo = self.expresion.interpretar(tree,table)
        result = table.getVariable(self.nombre)
        if isinstance(result.valor, dict):
            dicttmp = result.valor
            if dicttmp['mutable']:
                for i in self.atributos:
                    if dicttmp['mutable']:
                        if i == self.atributos[-1]:
                            if i in dicttmp['atributos']:
                                dicttmp['atributos'][i]=nuevo
                            else:
                                return Excepcion("Semantico", i+" No es un atributo de "+self.nombre,self.fila,self.columna)
                        elif i in dicttmp['atributos']:
                            dicttmp = dicttmp['atributos'][i]
                        else:
                            return Excepcion("Semantico", i+" No es un atributo de "+self.nombre,self.fila,self.columna)
                    else:
                        return Excepcion("Semantico", i+" Struct Inmutable",self.fila,self.columna)
            else:
                return Excepcion("Semantico", self.nombre+" Struct Inmutable",self.fila,self.columna)
        else:
            return Excepcion("Semantico", "Variable sin atributos",self.fila,self.columna)
        return None

    def getNodo(self):
        nodo1 = NodoAST("MODIFICAR STRUCT")
        nodoi = NodoAST("IDENTIFICADOR")
        nodoi.agregarHijo(self.nombre)
        nodo1.agregarHijoNodo(nodoi)
        nodo = NodoAST("ATRIBUTOS")
        for i in self.atributos:
            if i == self.atributos[0]:
                instruccioness3 = NodoAST("ATRIBUTO")
                instruccioness3.agregarHijo(i)
                nodo.agregarHijo(".")
                nodo.agregarHijoNodo(instruccioness3)
            else:
                instrtmp = nodo
                instruccioness3 = NodoAST("ATRIBUTO")
                nodo = NodoAST("ATRIBUTOS")
                nodo.agregarHijoNodo(instrtmp)
                nodo.agregarHijo(".")
                instruccioness3.agregarHijo(i)
                nodo.agregarHijoNodo(instruccioness3)
        nodo1.agregarHijoNodo(nodo)
        nodo1.agregarHijo("=")
        nodo1.agregarHijoNodo(self.expresion.getNodo())
        nodo1.agregarHijo(";")
        return nodo1
