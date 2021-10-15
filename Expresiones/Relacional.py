from enum import Enum
from os import truncate
from Abstract.ReturnA import Return
from Expresiones.Primitivo import Primitivo
from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from TS.GCI import Generator
from TS.Tipo import TIPOS

class Relacional(Expresion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        Expresion.__init__(self,None,fila,columna)
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer

    
    def interpretar(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()

        generator.addComment("INICIO EXPRESION RELACIONAL")
        res_left = self.OperacionIzq.interpretar(tree, table)
        res_right = None
        result = Return(None, TIPOS.BOOLEANO, False)
        if isinstance(res_left, Excepcion):
            return res_left
        if isinstance(res_right, Excepcion):
            return res_right

        if res_left.tipo != TIPOS.BOOLEANO:
            res_right = self.OperacionDer.interpretar(tree, table)
            if (res_left.tipo == TIPOS.ENTERO or res_left.tipo == TIPOS.DECIMAL) and (res_right.tipo == TIPOS.ENTERO or res_right.tipo == TIPOS.DECIMAL):
                self.checkLabels()
                generator.addIf(res_left.valor, res_right.valor, self.returnTipo(), self.ev)
                generator.addGoto(self.ef)
            elif res_left.tipo == TIPOS.CADENA and res_right.tipo == TIPOS.CADENA:
                if self.operador==OperadorRelacional.IGUALIGUAL:
                    generator.fcompareString()
                    tempP = generator.addTemp()
                    generator.addExp(tempP,'P',table.tamano,"+")
                    generator.addExp(tempP,tempP,'1',"+")
                    generator.setStack(tempP,res_left.valor)
                    generator.addExp(tempP,tempP,'1',"+")
                    generator.setStack(tempP,res_right.valor)
                    generator.newEnv(table.tamano)
                    generator.callFun('compareString')
                    tempC = generator.addTemp()
                    generator.getStack(tempC,'P')
                    generator.retEnv(table.tamano)
                    self.checkLabels()
                    generator.addIf(tempC, '1', '==', self.ev)
                    generator.addGoto(self.ef)
                elif self.operador==OperadorRelacional.DIFERENTE:
                    generator.fcompareString()
                    tempP = generator.addTemp()
                    generator.addExp(tempP,'P',table.tamano,"+")
                    generator.addExp(tempP,tempP,'1',"+")
                    generator.setStack(tempP,res_left.valor)
                    generator.addExp(tempP,tempP,'1',"+")
                    generator.setStack(tempP,res_right.valor)
                    generator.newEnv(table.tamano)
                    generator.callFun('compareString')
                    tempC = generator.addTemp()
                    generator.getStack(tempC,'P')
                    generator.retEnv(table.tamano)
                    self.checkLabels()
                    generator.addIf(tempC, '0', '==', self.ev)
                    generator.addGoto(self.ef)
        else:
            gotoRight = generator.newE()
            leftTemp = generator.addTemp()

            generator.putE(res_left.ev)
            generator.addExp(leftTemp, '1', '', '')
            generator.addGoto(gotoRight)

            generator.putE(res_left.ef)
            generator.addExp(leftTemp, '0', '', '')

            generator.putE(gotoRight)
            res_right = self.OperacionDer.interpretar(tree, table)
            if res_right.tipo != TIPOS.BOOLEANO:
                print("Error, no se pueden comparar")
                return
            gotoEnd = generator.newE()
            rightTemp = generator.addTemp()

            generator.putE(res_right.ev)
            
            generator.addExp(rightTemp, '1', '', '')
            generator.addGoto(gotoEnd)

            generator.putE(res_right.ef)
            generator.addExp(rightTemp, '0', '', '')

            generator.putE(gotoEnd)

            self.checkLabels()
            generator.addIf(leftTemp, rightTemp, self.returnTipo(), self.ev)
            generator.addGoto(self.ef)

        generator.addComment("FIN DE EXPRESION RELACIONAL")
        generator.addSpace()
        result.ev = self.ev
        result.ef = self.ef

        return result     

    def getNodo(self):
        nodo = NodoAST("RELACIONAL")
        if self.OperacionDer != None:
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
            op = self.returnTipo()
            nodo.agregarHijo(op)
            nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo("-")
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
        
        return nodo

    def returnTipo(self):
        ret=""
        if self.operador==OperadorRelacional.MENORQUE:
            ret="<"
        elif self.operador==OperadorRelacional.MAYORQUE:
            ret=">"
        elif self.operador==OperadorRelacional.MENORIGUAL:
            ret="<="
        elif self.operador==OperadorRelacional.MAYORIGUAL:
            ret=">="
        elif self.operador==OperadorRelacional.IGUALIGUAL:
            ret="=="
        elif self.operador==OperadorRelacional.DIFERENTE:
            ret="!="
        return ret

    def obtenerVal(self, tipo, val):
        if tipo == TIPOS.ENTERO:
            return int(val)
        elif tipo == TIPOS.DECIMAL:
            return float(val)
        elif tipo == TIPOS.BOOLEANO:
            return bool(val)
        return str(val)
        
    def checkLabels(self):
        genAux = Generator()
        generator = genAux.getInstance()
        if self.ev == '':
            self.ev = generator.newE()
        if self.ef == '':
            self.ef = generator.newE()

class OperadorRelacional(Enum):
    MENORQUE = 1
    MAYORQUE = 2
    MENORIGUAL = 3
    MAYORIGUAL = 4
    IGUALIGUAL = 5
    DIFERENTE = 6