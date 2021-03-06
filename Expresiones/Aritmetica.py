from Abstract.ReturnA import Return
from Expresiones.Primitivo import Primitivo
from enum import Enum
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Expresion
from Excepciones.Excepcion import Excepcion
from Instrucciones.Llamada import Llamada
from TS.TCI import TCI
from TS.Tipo import TIPOS


class Aritmetica(Expresion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        res_left = None
        res_right = None
        res_uni = None
        if self.OperacionDer is not None:
            res_left = self.OperacionIzq.interpretar(tree, table)
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
            if isinstance(res_left, Excepcion):
                return res_left
            if isinstance(res_right, Excepcion):
                return res_right;  
        else:
            res_uni = self.OperacionIzq.interpretar(tree, table)
        temp = codigoR.addTemp()
        op = ''
        if (self.operador==OperadorAritmetico.MAS):
            op = '+'
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.ENTERO, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    tree.excepciones.append()
                    return Excepcion("Semantico", "Tipo erroneo para +",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para +",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para +",self.fila,self.columna)
        
        elif (self.operador==OperadorAritmetico.MENOS):
            op = '-'
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.ENTERO, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para -",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para -",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para -",self.fila,self.columna)
        
        elif (self.operador==OperadorAritmetico.POR):
            op = '*'
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.ENTERO, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para *4",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    codigoR.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para *5",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.CADENA):
                if(res_right.tipo==TIPOS.CADENA):
                    codigoR.fconString()
                    paramTemp = codigoR.addTemp()
                    codigoR.addExp(paramTemp, 'P', table.tamano, '+')
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_left.valor)
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_right.valor)
                    codigoR.newEnv(table.tamano)
                    codigoR.callFun('addString')
                    paramTemp = codigoR.addTemp()
                    codigoR.getStack(paramTemp, 'P')
                    codigoR.retEnv(table.tamano)
                    return Return(paramTemp, TIPOS.CADENA, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para *1",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para *2",self.fila,self.columna)
        
        elif (self.operador==OperadorAritmetico.DIV):
            op='/'
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    temp1 = codigoR.addTemp()
                    res_left.valor = str(res_left.valor)
                    codigoR.addExp(temp1, res_left.valor,'','')
                    temp2 = codigoR.addTemp()
                    res_right.valor = str(res_right.valor)
                    codigoR.addExp(temp2, res_right.valor,'','')
                    okE = codigoR.newE()
                    badE = codigoR.newE()
                    outE = codigoR.newE()
                    codigoR.addIf(temp2,'0','!=',okE)
                    codigoR.GoTo(badE)
                    codigoR.putE(okE)
                    codigoR.addExp(temp, temp1,temp2,op)
                    codigoR.GoTo(outE)
                    codigoR.putE(badE)
                    codigoR.printMathE()
                    codigoR.callFun('MathError')
                    codigoR.addExp(temp, '0','','')
                    codigoR.GoTo(outE)
                    codigoR.putE(outE)
                    return Return(temp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    temp1 = codigoR.addTemp()
                    res_left.valor = str(res_left.valor)
                    codigoR.addExp(temp1, res_left.valor,'','')
                    temp2 = codigoR.addTemp()
                    res_right.valor = str(res_right.valor)
                    codigoR.addExp(temp2, res_right.valor,'','')
                    okE = codigoR.newE()
                    badE = codigoR.newE()
                    outE = codigoR.newE()
                    codigoR.addIf(temp2,'0','!=',okE)
                    codigoR.GoTo(badE)
                    codigoR.putE(okE)
                    codigoR.addExp(temp, temp1,temp2,op)
                    codigoR.GoTo(outE)
                    codigoR.putE(badE)
                    codigoR.printMathE()
                    codigoR.callFun('MathError')
                    codigoR.addExp(temp, '0','','')
                    codigoR.GoTo(outE)
                    codigoR.putE(outE)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para /",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    temp1 = codigoR.addTemp()
                    res_left.valor = str(res_left.valor)
                    codigoR.addExp(temp1, res_left.valor,'','')
                    temp2 = codigoR.addTemp()
                    res_right.valor = str(res_right.valor)
                    codigoR.addExp(temp2, res_right.valor,'','')
                    okE = codigoR.newE()
                    badE = codigoR.newE()
                    outE = codigoR.newE()
                    codigoR.addIf(temp2,'0','!=',okE)
                    codigoR.GoTo(badE)
                    codigoR.putE(okE)
                    codigoR.addExp(temp, temp1,temp2,op)
                    codigoR.GoTo(outE)
                    codigoR.putE(badE)
                    codigoR.printMathE()
                    codigoR.callFun('MathError')
                    codigoR.addExp(temp, '0','','')
                    codigoR.GoTo(outE)
                    codigoR.putE(outE)
                    return Return(temp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    temp1 = codigoR.addTemp()
                    res_left.valor = str(res_left.valor)
                    codigoR.addExp(temp1, res_left.valor,'','')
                    temp2 = codigoR.addTemp()
                    res_right.valor = str(res_right.valor)
                    codigoR.addExp(temp2, res_right.valor,'','')
                    okE = codigoR.newE()
                    badE = codigoR.newE()
                    outE = codigoR.newE()
                    codigoR.addIf(temp2,'0','!=',okE)
                    codigoR.GoTo(badE)
                    codigoR.putE(okE)
                    codigoR.addExp(temp, temp1,temp2,op)
                    codigoR.GoTo(outE)
                    codigoR.putE(badE)
                    codigoR.printMathE()
                    codigoR.callFun('MathError')
                    codigoR.addExp(temp, '0','','')
                    codigoR.GoTo(outE)
                    codigoR.putE(outE)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para /",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para /",self.fila,self.columna)
        elif (self.operador==OperadorAritmetico.POT):
            op='^'
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    codigoR.fPow()
                    paramTemp = codigoR.addTemp()
                    codigoR.addExp(paramTemp, 'P', table.tamano, '+')
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_left.valor)
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_right.valor)
                    codigoR.newEnv(table.tamano)
                    codigoR.callFun('Pow')
                    paramTemp = codigoR.addTemp()
                    codigoR.getStack(paramTemp, 'P')
                    codigoR.retEnv(table.tamano)
                    return Return(paramTemp, TIPOS.ENTERO, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    codigoR.fPow()
                    paramTemp = codigoR.addTemp()
                    codigoR.addExp(paramTemp, 'P', table.tamano, '+')
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_left.valor)
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_right.valor)
                    codigoR.newEnv(table.tamano)
                    codigoR.callFun('Pow')
                    paramTemp = codigoR.addTemp()
                    codigoR.getStack(paramTemp, 'P')
                    codigoR.retEnv(table.tamano)
                    return Return(paramTemp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para ^",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    codigoR.fPow()
                    paramTemp = codigoR.addTemp()
                    codigoR.addExp(paramTemp, 'P', table.tamano, '+')
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_left.valor)
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_right.valor)
                    codigoR.newEnv(table.tamano)
                    codigoR.callFun('Pow')
                    paramTemp = codigoR.addTemp()
                    codigoR.getStack(paramTemp, 'P')
                    codigoR.retEnv(table.tamano)
                    return Return(paramTemp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    codigoR.fPow()
                    paramTemp = codigoR.addTemp()
                    codigoR.addExp(paramTemp, 'P', table.tamano, '+')
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_left.valor)
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_right.valor)
                    codigoR.newEnv(table.tamano)
                    codigoR.callFun('Pow')
                    paramTemp = codigoR.addTemp()
                    codigoR.getStack(paramTemp, 'P')
                    codigoR.retEnv(table.tamano)
                    return Return(paramTemp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para ^",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.CADENA):
                if(res_right.tipo==TIPOS.ENTERO):
                    codigoR.fpowString()
                    paramTemp = codigoR.addTemp()
                    codigoR.addExp(paramTemp, 'P', table.tamano, '+')
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_left.valor)
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, res_right.valor)
                    codigoR.newEnv(table.tamano)
                    codigoR.callFun('powString')
                    paramTemp = codigoR.addTemp()
                    codigoR.getStack(paramTemp, 'P')
                    codigoR.retEnv(table.tamano)
                    return Return(paramTemp, TIPOS.CADENA, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para ^",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para ^",self.fila,self.columna)
        
        elif (self.operador==OperadorAritmetico.MOD):
            op='%'
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    codigoR.addMod(temp, res_left.valor,res_right.valor)
                    return Return(temp, TIPOS.ENTERO, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    codigoR.addMod(temp, res_left.valor,res_right.valor)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para %",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    codigoR.addMod(temp, res_left.valor,res_right.valor)
                    return Return(temp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    codigoR.addMod(temp, res_left.valor,res_right.valor)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para %",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para %",self.fila,self.columna)
        
        elif (self.operador==OperadorAritmetico.UNMENOS):
            op='*'
            if(res_uni.tipo==TIPOS.ENTERO):
                codigoR.addExp(temp, res_uni.valor,-1,op)
                return Return(temp, TIPOS.ENTERO, True)
            elif(res_uni.tipo==TIPOS.DECIMAL):
                codigoR.addExp(temp, res_uni.valor,-1,op)
                return Return(temp, TIPOS.DECIMAL, True)
            else:
                return Excepcion("Semantico", "Tipo erroneo para negativo",self.fila,self.columna)
        '''return Excepcion("Semantico", "Operador desconocido",self.fila,self.columna)'''

    def getNodo(self):
        nodo = NodoAST("ARITMETICA")
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
        if self.operador==OperadorAritmetico.MAS:
            ret="+"
        elif self.operador==OperadorAritmetico.MENOS:
            ret="-"
        elif self.operador==OperadorAritmetico.POR:
            ret="*"
        elif self.operador==OperadorAritmetico.DIV:
            ret="/"
        elif self.operador==OperadorAritmetico.POT:
            ret="^"
        elif self.operador==OperadorAritmetico.MOD:
            ret="%"
        return ret

class OperadorAritmetico(Enum):
    MAS = 1
    MENOS = 2
    POR = 3
    DIV = 4
    POT = 5
    MOD = 6
    UNMENOS = 7