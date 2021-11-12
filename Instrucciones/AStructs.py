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


class AStruct(Expresion):
    def __init__(self, nombre, atributos, fila, columna):
        self.nombre = nombre
        self.atributos = atributos
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        result = table.getVariable(self.nombre)
        temp1 = codigoR.addTemp()
        temp2 = result.posicion
        if(not result.globalV):
            temp2 = codigoR.addTemp()
            codigoR.addExp(temp2, 'P', result.posicion, "+")
        codigoR.getStack(temp1,temp2)
        dicttmp2 = table.getStruct(result.tipoS)
        posicion = 0
        tipo = None
        retorno=None
        tmp = dicttmp2['atributos'].keys()
        tempAux = codigoR.addTemp()
        retorno = codigoR.addTemp()
        for i in self.atributos:
            posicion=0
            for att in tmp:
                    if att == i:
                        break
                    posicion = posicion + 1
            tipo = dicttmp2['atributos'][i]
            codigoR.addExp(tempAux, temp1, posicion, '+')
            codigoR.getHeap(retorno, tempAux)
            if i == self.atributos[-1]:
                if isinstance(tipo,list):
                    return Return(retorno, TIPOS.ARREGLO, True,tipo)
                else:
                    return Return(retorno, tipo, True)
            else:
                dicttmp2 = table.getStruct(tipo)
                tmp = dicttmp2['atributos'].keys()
                codigoR.addExp(temp1, retorno, '', '')
                
        
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
