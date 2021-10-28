import copy
from Expresiones.Identificador import Identificador
from Abstract.instruccion import Expresion
from Instrucciones.Return import ReturnI
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from TS.TCI import TCI
from TS.Tipo import TIPO, TIPOS
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from TS.Simbolo import Simbolo

class MArreglos(Expresion):
    def __init__(self, identificador, posiciones, expresion, fila, columna):
        self.identificador = identificador
        self.posiciones = posiciones
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        result = Identificador(self.identificador,self.fila,self.columna)
        result = result.interpretar(tree,table)
        if result.tipo==TIPOS.ARREGLO:
            codigoAux = TCI()
            codigoR = codigoAux.getInstance()
            temp2 = None
            temp1 = None
            listtmp = None
            if isinstance(result.aux, list):
                if len(result.aux) != len(self.posiciones):
                    listtmp = copy.deepcopy(result.aux)
                    for i in range(len(self.posiciones)):
                        listtmp.pop(i)
                for i in self.posiciones:
                    iC = i.interpretar(tree,table)
                    temp1 = codigoR.addTemp()
                    if i == self.posiciones[0]:
                        codigoR.addExp(temp1, result.valor,iC.valor, "+")
                        temp2 = codigoR.addTemp()
                        codigoR.getHeap(temp2,temp1)
                    elif i != self.posiciones[-1]:
                        codigoR.addExp(temp1, temp2,iC.valor, "+")
                        temp2 = codigoR.addTemp()
                        codigoR.getHeap(temp2,temp1)
                    else:
                        codigoR.addExp(temp1, temp2,iC.valor, "+")
                retorno = self.expresion.interpretar(tree,table)
                codigoR.setHeap(temp1,retorno.valor)
        else:
            return Excepcion("Semantico", "Variable no es un Arreglo", self.fila, self.columna)

    def getNodo(self):
        nodo1 = NodoAST("MODIFICARVECTOR")
        nodoi = NodoAST("IDENTIFICADOR")
        nodoi.agregarHijo(self.identificador)
        nodo1.agregarHijoNodo(nodoi)
        nodo = NodoAST("varios_cor")
        for i in self.posiciones:
            if i == self.posiciones[0]:
                instruccioness3 = NodoAST("EXPRESION")
                instruccioness3.agregarHijoNodo(i.getNodo())
                nodo.agregarHijo("[")
                nodo.agregarHijoNodo(instruccioness3)
                nodo.agregarHijo("]")
            else:
                instrtmp = nodo
                instruccioness3 = NodoAST("EXPRESION")
                nodo = NodoAST("varios_cor")
                nodo.agregarHijoNodo(instrtmp)
                nodo.agregarHijo("[")
                instruccioness3.agregarHijoNodo(i.getNodo())
                nodo.agregarHijoNodo(instruccioness3)
                nodo.agregarHijo("]")
        nodo1.agregarHijoNodo(nodo)
        nodo1.agregarHijo("=")
        nodo1.agregarHijoNodo(self.expresion.getNodo())
        nodo1.agregarHijo(";")
        return nodo1
