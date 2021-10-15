from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Expresion
from Abstract.ReturnA import Return
from abc import ABC, abstractmethod
from TS.GCI import Generator
from TS.Tipo import TIPOS


class Primitivo(Expresion):
    def __init__(self, tipo, valor, fila, columna):
        Expresion.__init__(self,tipo,fila,columna)
        self.valor=valor

    def interpretar(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()
        if(self.tipo==TIPOS.ENTERO or self.tipo==TIPOS.DECIMAL):
            return Return(str(self.valor),self.tipo,False)
        elif self.tipo == TIPOS.BOOLEANO:
            if self.ev == '':
                self.ev = generator.newE()
            if self.ef == '':
                self.ef = generator.newE()
            
            if(self.valor):
                generator.addGoto(self.ev)
                generator.addComment("GOTO PARA EVITAR ERROR DE GO")
                generator.addGoto(self.ef)
            else:
                generator.addGoto(self.ef)
                generator.addComment("GOTO PARA EVITAR ERROR DE GO")
                generator.addGoto(self.ev)
            
            ret = Return(self.valor, self.tipo, False)
            ret.ev = self.ev
            ret.ef = self.ef

            return ret
        elif self.tipo == TIPOS.CADENA:
            retTemp = generator.addTemp()
            generator.addExp(retTemp, 'H', '', '')

            for char in str(self.valor):
                generator.setHeap('H', ord(char))   # heap[H] = NUM;
                generator.nextHeap()                # H = H + 1;

            generator.setHeap('H', '-1')            # FIN DE CADENA
            generator.nextHeap()

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