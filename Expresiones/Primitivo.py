from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Expresion
from Abstract.ReturnA import Return
from abc import ABC, abstractmethod
from TS.TCI import TCI
from TS.Tipo import TIPOS


class Primitivo(Expresion):
    def __init__(self, tipo, valor, fila, columna):
        Expresion.__init__(self,tipo,fila,columna)
        self.valor=valor

    def interpretar(self, tree, table):
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        if(self.tipo==TIPOS.ENTERO or self.tipo==TIPOS.DECIMAL):
            return Return(str(self.valor),self.tipo,False)
        elif self.tipo == TIPOS.BOOLEANO:
            if self.ev == '':
                self.ev = codigoR.newE()
            if self.ef == '':
                self.ef = codigoR.newE()
            
            if(self.valor):
                codigoR.GoTo(self.ev)
                codigoR.addComment("GOTO PARA EVITAR ERROR DE GO")
                codigoR.GoTo(self.ef)
            else:
                codigoR.GoTo(self.ef)
                codigoR.addComment("GOTO PARA EVITAR ERROR DE GO")
                codigoR.GoTo(self.ev)
            
            ret = Return(self.valor, self.tipo, False)
            ret.ev = self.ev
            ret.ef = self.ef

            return ret
        elif self.tipo == TIPOS.CADENA:
            retTemp = codigoR.addTemp()
            codigoR.addExp(retTemp, 'H', '', '')

            for char in str(self.valor):
                codigoR.setHeap('H', ord(char))   # heap[H] = NUM;
                codigoR.nextHeap()                # H = H + 1;

            codigoR.setHeap('H', '-1')            # FIN DE CADENA
            codigoR.nextHeap()

            return Return(retTemp, TIPOS.CADENA, True)

    def getNodo(self):
        nodo1 = NodoAST("PRIMITIVO")
        if self.valor is None:
            nodo1.agregarHijo("Nothing")
        else:
            if isinstance(self.valor,list):
                nodo1.agregarHijo("[")
                nodo = NodoAST("varias_coma")
                for i in self.valor:
                    if i == self.valor[0]:
                        instruccioness3 = NodoAST("EXPRESION")
                        instruccioness3.agregarHijoNodo(i.getNodo())
                        nodo.agregarHijoNodo(instruccioness3)
                    else:
                        instrtmp = nodo
                        instruccioness3 = NodoAST("EXPRESION")
                        nodo = NodoAST("varias_coma")
                        nodo.agregarHijoNodo(instrtmp)
                        nodo.agregarHijo(",")
                        instruccioness3.agregarHijoNodo(i.getNodo())
                        nodo.agregarHijoNodo(instruccioness3)
                nodo1.agregarHijoNodo(nodo)
                nodo1.agregarHijo("]")
            else:
                nodo1.agregarHijo(self.valor)
        return nodo1