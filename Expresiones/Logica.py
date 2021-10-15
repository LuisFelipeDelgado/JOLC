from enum import Enum
from Abstract.ReturnA import Return
from Expresiones.Primitivo import Primitivo
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Expresion
from Excepciones.Excepcion import Excepcion
from TS.GCI import Generator
from TS.Tipo import TIPOS

class Logica(Expresion):
    def __init__(self, operador, OperacionIzq, fila, columna, OperacionDer=None):
        Expresion.__init__(self,None,fila,columna)
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer

    def interpretar(self, tree, table):
        res_left = None
        res_right = None
        res_uni = None
        genAux = Generator()
        generator = genAux.getInstance()
        generator.addComment("INICIO EXPRESION LOGICA")
        self.checkLabels()
        lblAndOr = ''
        if (self.operador==OperadorLogico.OR):
            self.OperacionIzq.ev = self.OperacionDer.ev = self.ev
            lblAndOr = self.OperacionIzq.ef = generator.newE()
            self.OperacionDer.ef = self.ef
                    
        elif (self.operador==OperadorLogico.AND):
            lblAndOr = self.OperacionIzq.ev = generator.newE()
            self.OperacionDer.ev = self.ev
            self.OperacionIzq.ef = self.OperacionDer.ef = self.ef
        
        elif (self.operador==OperadorLogico.NOT):
            lblAndOr = self.OperacionIzq.ef = self.ev
            self.OperacionIzq.ev = self.ef
            res_uni = self.OperacionIzq.interpretar(tree, table)
            generator.addComment("FINALIZO EXPRESION LOGICA")
            generator.addSpace()
            ret = Return(None, TIPOS.BOOLEANO, False)
            ret.ev = self.ev
            ret.ef = self.ef
            return ret
        res_left = self.OperacionIzq.interpretar(tree, table)
        if res_left.tipo != TIPOS.BOOLEANO:
            print("No se puede utilizar en expresion booleana")
            return
        generator.putE(lblAndOr)
        res_right = self.OperacionDer.interpretar(tree,table)
        if res_right.tipo != TIPOS.BOOLEANO:
            print("No se puede utilizar en expresion booleana")
            return
        generator.addComment("FINALIZO EXPRESION LOGICA")
        generator.addSpace()
        ret = Return(None, TIPOS.BOOLEANO, False)
        ret.ev = self.ev
        ret.ef = self.ef
        return ret


    def getNodo(self):
        nodo = NodoAST("RELACIONAL")
        if self.OperacionDer != None:
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
            op = self.returnTipo()
            nodo.agregarHijo(op)
            nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo("!")
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
        
        return nodo

    def returnTipo(self):
        ret=""
        if self.operador==OperadorLogico.AND:
            ret="&&"
        elif self.operador==OperadorLogico.OR:
            ret="||"
        return ret

    def checkLabels(self):
        genAux = Generator()
        generator = genAux.getInstance()
        if self.ev == '':
            self.ev = generator.newE()
        if self.ef == '':
            self.ef = generator.newE()
            
class OperadorLogico(Enum):
    NOT = 1
    AND = 2
    OR = 3