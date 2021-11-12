from enum import Enum
from os import truncate
from Abstract.ReturnA import Return
from Expresiones.Primitivo import Primitivo
from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from Instrucciones.Llamada import Llamada
from TS.TCI import TCI
from TS.Tipo import TIPOS

class Relacional(Expresion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        Expresion.__init__(self,None,fila,columna)
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer

    
    def interpretar(self, tree, table):
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()

        codigoR.addComment("INICIO EXPRESION RELACIONAL")
        res_left = self.OperacionIzq.interpretar(tree, table)
        res_right = None
        result = Return(None, TIPOS.BOOLEANO, False)
        if isinstance(res_left, Excepcion):
            return res_left
        if isinstance(res_right, Excepcion):
            return res_right

        if res_left.tipo != TIPOS.BOOLEANO:
            if table.funcion and isinstance(self.OperacionDer,Llamada):
                    tempP = codigoR.addTemp()
                    codigoR.addExp(tempP,'P',table.tamano,'+')
                    codigoR.setStack(tempP,res_left.valor)
                    table.tamano += 1
                    res_right = self.OperacionDer.interpretar(tree, table)
                    table.tamano -= 1
                    tempP = codigoR.addTemp()
                    codigoR.addExp(tempP,'P',table.tamano,'+')
                    codigoR.getStack(res_left.valor,tempP)
            else:
                res_right = self.OperacionDer.interpretar(tree, table)
            if (res_left.tipo == TIPOS.ENTERO or res_left.tipo == TIPOS.DECIMAL) and (res_right.tipo == TIPOS.ENTERO or res_right.tipo == TIPOS.DECIMAL):
                self.checkLabels()
                codigoR.addIf(res_left.valor, res_right.valor, self.returnTipo(), self.ev)
                codigoR.GoTo(self.ef)
            elif (res_left.tipo == TIPOS.NULO or res_right.tipo == TIPOS.NULO):
                self.checkLabels()
                codigoR.addIf(res_left.valor, res_right.valor, self.returnTipo(), self.ev)
                codigoR.GoTo(self.ef)
            elif res_left.tipo == TIPOS.CADENA and res_right.tipo == TIPOS.CADENA:
                if self.operador==OperadorRelacional.IGUALIGUAL:
                    codigoR.fcompareString()
                    tempP = codigoR.addTemp()
                    codigoR.addExp(tempP,'P',table.tamano,"+")
                    codigoR.addExp(tempP,tempP,'1',"+")
                    codigoR.setStack(tempP,res_left.valor)
                    codigoR.addExp(tempP,tempP,'1',"+")
                    codigoR.setStack(tempP,res_right.valor)
                    codigoR.newEnv(table.tamano)
                    codigoR.callFun('compareString')
                    tempC = codigoR.addTemp()
                    codigoR.getStack(tempC,'P')
                    codigoR.retEnv(table.tamano)
                    self.checkLabels()
                    codigoR.addIf(tempC, '1', '==', self.ev)
                    codigoR.GoTo(self.ef)
                elif self.operador==OperadorRelacional.DIFERENTE:
                    codigoR.fcompareString()
                    tempP = codigoR.addTemp()
                    codigoR.addExp(tempP,'P',table.tamano,"+")
                    codigoR.addExp(tempP,tempP,'1',"+")
                    codigoR.setStack(tempP,res_left.valor)
                    codigoR.addExp(tempP,tempP,'1',"+")
                    codigoR.setStack(tempP,res_right.valor)
                    codigoR.newEnv(table.tamano)
                    codigoR.callFun('compareString')
                    tempC = codigoR.addTemp()
                    codigoR.getStack(tempC,'P')
                    codigoR.retEnv(table.tamano)
                    self.checkLabels()
                    codigoR.addIf(tempC, '0', '==', self.ev)
                    codigoR.GoTo(self.ef)
        else:
            gotoRight = codigoR.newE()
            leftTemp = codigoR.addTemp()

            codigoR.putE(res_left.ev)
            codigoR.addExp(leftTemp, '1', '', '')
            codigoR.GoTo(gotoRight)

            codigoR.putE(res_left.ef)
            codigoR.addExp(leftTemp, '0', '', '')

            codigoR.putE(gotoRight)
            if table.funcion and isinstance(self.OperacionDer,Llamada):
                    tempP = codigoR.addTemp()
                    codigoR.addExp(tempP,'P',table.tamano,'+')
                    codigoR.setStack(tempP,res_left.valor)
                    table.tamano += 1
                    res_right = self.OperacionDer.interpretar(tree, table)
                    table.tamano -= 1
                    tempP = codigoR.addTemp()
                    codigoR.addExp(tempP,'P',table.tamano,'+')
                    codigoR.getStack(res_left.valor,tempP)
            else:
                res_right = self.OperacionDer.interpretar(tree, table)
            if res_right.tipo != TIPOS.BOOLEANO:
                print("Error, no se pueden comparar")
                return
            gotoEnd = codigoR.newE()
            rightTemp = codigoR.addTemp()

            codigoR.putE(res_right.ev)
            
            codigoR.addExp(rightTemp, '1', '', '')
            codigoR.GoTo(gotoEnd)

            codigoR.putE(res_right.ef)
            codigoR.addExp(rightTemp, '0', '', '')

            codigoR.putE(gotoEnd)

            self.checkLabels()
            codigoR.addIf(leftTemp, rightTemp, self.returnTipo(), self.ev)
            codigoR.GoTo(self.ef)

        codigoR.addComment("FIN DE EXPRESION RELACIONAL")
        codigoR.addSpace()
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
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        if self.ev == '':
            self.ev = codigoR.newE()
        if self.ef == '':
            self.ef = codigoR.newE()

class OperadorRelacional(Enum):
    MENORQUE = 1
    MAYORQUE = 2
    MENORIGUAL = 3
    MAYORIGUAL = 4
    IGUALIGUAL = 5
    DIFERENTE = 6