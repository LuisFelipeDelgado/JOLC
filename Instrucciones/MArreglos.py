from Expresiones.Identificador import Identificador
from Abstract.instruccion import Expresion
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
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
            if isinstance(result.valor, list):
                listtmp = result.valor
                for i in self.posiciones:
                    iC = i.interpretar(tree,table)
                    iC = iC.valor
                    tmp = listtmp[iC-1].interpretar(tree,table)
                    if isinstance(tmp.valor, list):
                        if i == self.posiciones[-1]:
                            retorno = self.expresion.interpretar(tree,table)
                            listtmp[iC-1] = retorno
                            return None
                        listtmp = tmp.valor
                    elif i == self.posiciones[-1]:
                        retorno = self.expresion.interpretar(tree,table)
                        listtmp[iC-1] = retorno
                        return None
                return None
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
