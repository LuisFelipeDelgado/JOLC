from TS.Simbolo import Simbolo
from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPOS
from Instrucciones.Return import ReturnI
from Excepciones.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class AStruct(Expresion):
    def __init__(self, nombre, atributos, fila, columna):
        self.nombre = nombre
        self.atributos = atributos
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        result = table.getVariable(self.nombre)
        dicttmp2 = result.valor
        if isinstance(dicttmp2, dict):
            for i in self.atributos:
                if i == self.atributos[-1]:
                    return dicttmp2['atributos'][i]
                if i in dicttmp2['atributos']:
                    dicttmp2 = dicttmp2['atributos'][i]
                else:
                    return Excepcion("Semantico", i+" No es un atributo de "+self.nombre,self.fila,self.columna)
        else:
            return Excepcion("Semantico", "Variable sin atributos",self.fila,self.columna)
        declara = Simbolo(TIPOS.STRUCT, self.nombre, self.fila, self.columna, self.atributos)
        result = table.actualizarTabla(declara)
        return None

    def getNodo(self):
        nodo1 = NodoAST("ACCEDER STRUCT")
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
        return nodo1
