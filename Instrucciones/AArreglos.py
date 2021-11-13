from Expresiones.Identificador import Identificador
from Abstract.instruccion import Expresion
from Abstract.ReturnA import Return
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from TS.TCI import TCI
from TS.Tipo import TIPO, TIPOS
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from TS.Simbolo import Simbolo
import copy

class AArreglos(Expresion):
    def __init__(self, identificador, posiciones, fila, columna):
        self.identificador = identificador
        self.posiciones = posiciones
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
                salidaE = codigoR.newE()
                if len(result.aux) != len(self.posiciones):
                    listtmp = copy.deepcopy(result.aux)
                    for i in range(len(self.posiciones)):
                        listtmp.pop(i)
                for i in self.posiciones:
                    errorE = codigoR.newE()
                    continuarE = codigoR.newE()
                    iC = i.interpretar(tree,table)
                    temp1 = codigoR.addTemp()
                    temp3 = codigoR.addTemp()
                    if i == self.posiciones[0]:
                        codigoR.getHeap(temp3,result.valor)
                        codigoR.addIf(iC.valor,temp3,'>',errorE)
                        codigoR.addExp(temp1, result.valor,iC.valor, "+")
                        temp2 = codigoR.addTemp()
                        codigoR.getHeap(temp2,temp1)
                        codigoR.GoTo(continuarE)
                        codigoR.putE(errorE)
                        codigoR.printBoundsE()
                        codigoR.callFun('BoundsError')
                        codigoR.addExp(temp2, '0','', '')
                        codigoR.GoTo(salidaE)
                        codigoR.putE(continuarE)
                    else:
                        codigoR.getHeap(temp3,temp2)
                        codigoR.addIf(iC.valor,temp3,'>',errorE)
                        codigoR.addExp(temp1, temp2,iC.valor, "+")
                        temp2 = codigoR.addTemp()
                        codigoR.getHeap(temp2,temp1)
                        codigoR.GoTo(continuarE)
                        codigoR.putE(errorE)
                        codigoR.printBoundsE()
                        codigoR.callFun('BoundsError')
                        codigoR.addExp(temp2, '0','', '')
                        codigoR.GoTo(salidaE)
                        codigoR.putE(continuarE)
                codigoR.putE(salidaE)
                return Return(temp2,(result.aux[len(self.posiciones)-1]),True,listtmp)
        else:
            return Excepcion("Semantico", "Variable no es un Arreglo", self.fila, self.columna)

    def getNodo(self):
        nodo1 = NodoAST("ACCESOVECTOR")
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
        return nodo1
