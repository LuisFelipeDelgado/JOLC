from copy import copy
from Abstract.ReturnA import Return
from TS.Simbolo import Simbolo
from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from TS.TCI import TCI
from TS.Tipo import TIPOS
from Instrucciones.Return import ReturnI
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
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        nuevo = self.expresion.interpretar(tree,table)
        result = table.getVariable(self.nombre)
        if result.tipo== TIPOS.STRUCT:
            temp1 = codigoR.addTemp()
            temp2 = codigoR.addTemp()
            codigoR.addExp(temp2, 'P', result.posicion, "+")
            codigoR.getStack(temp1,temp2)
            dicttmp = table.getStruct(result.tipoS)
            posicion = 0
            tipo = None
            retorno=None
            tmp = dicttmp['atributos'].keys()
            tempAux = codigoR.addTemp()
            retorno = codigoR.addTemp()
            if dicttmp['mutable']:
                for i in self.atributos:
                    if dicttmp['mutable']:
                        for att in tmp:
                            if att == i:
                                break
                            posicion = posicion + 1
                        tipo = dicttmp['atributos'][i]
                        codigoR.addExp(tempAux, temp1, posicion, '+')
                        if i == self.atributos[-1]:
                            codigoR.setHeap(tempAux,nuevo.valor)
                        else:
                            codigoR.getHeap(retorno, tempAux)
                            dicttmp = table.getStruct(tipo)
                            tmp = dicttmp['atributos'].keys()
                            codigoR.addExp(temp1, retorno, '', '')
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
