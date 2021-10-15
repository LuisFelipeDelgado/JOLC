from Abstract.ReturnA import Return
from Expresiones.Primitivo import Primitivo
from enum import Enum
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Expresion
from Excepciones.Excepcion import Excepcion
from TS.GCI import Generator
from TS.Tipo import TIPOS


class Aritmetica(Expresion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        genaux = Generator()
        generator = genaux.getInstance()
        res_left = None
        res_right = None
        res_uni = None
        if self.OperacionDer is not None:
            res_left = self.OperacionIzq.interpretar(tree, table)
            res_right = self.OperacionDer.interpretar(tree,table)
            if isinstance(res_left, Excepcion):
                return res_left
            if isinstance(res_right, Excepcion):
                return res_right;  
        else:
            res_uni = self.OperacionIzq.interpretar(tree, table)
        temp = generator.addTemp()
        op = ''
        if (self.operador==OperadorAritmetico.MAS):
            op = '+'
            if(res_left.tipo==TIPOS.ENTERO):
                print(res_left.valor)
                if(res_right.tipo==TIPOS.ENTERO):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.ENTERO, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    tree.excepciones.append()
                    return Excepcion("Semantico", "Tipo erroneo para +",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para +",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para +",self.fila,self.columna)
        
        elif (self.operador==OperadorAritmetico.MENOS):
            op = '-'
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.ENTERO, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para -",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para -",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para -",self.fila,self.columna)
        
        elif (self.operador==OperadorAritmetico.POR):
            op = '*'
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.ENTERO, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para *4",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para *5",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.CADENA):
                if(res_right.tipo==TIPOS.CADENA):
                    generator.fconString()
                    paramTemp = generator.addTemp()
                    generator.addExp(paramTemp, 'P', table.tamano, '+')
                    generator.addExp(paramTemp, paramTemp, '1', '+')
                    generator.setStack(paramTemp, res_left.valor)
                    generator.addExp(paramTemp, paramTemp, '1', '+')
                    generator.setStack(paramTemp, res_right.valor)
                    generator.newEnv(table.tamano)
                    generator.callFun('addString')
                    paramTemp = generator.addTemp()
                    generator.getStack(paramTemp, 'P')
                    generator.retEnv(table.tamano)
                    return Return(paramTemp, TIPOS.CADENA, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para *1",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para *2",self.fila,self.columna)
        
        elif (self.operador==OperadorAritmetico.DIV):
            op='/'
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    res_left.valor = int(res_left.valor)*1.0
                    res_left.valor = str(res_left.valor)
                    res_right.valor = int(res_right.valor)*1.0
                    res_right.valor = str(res_right.valor)
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    generator.addExp(temp, res_left.valor,res_right.valor,op)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para /",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    return Primitivo(TIPOS.DECIMAL, float(str(res_left.valor)) / int(str(res_right.valor)), self.fila, self.columna)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    return Primitivo(TIPOS.DECIMAL, float(str(res_left.valor)) / float(str(res_right.valor)), self.fila, self.columna)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para /",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para /",self.fila,self.columna)
        elif (self.operador==OperadorAritmetico.POT):
            op='^'
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    generator.fPow()
                    paramTemp = generator.addTemp()
                    generator.addExp(paramTemp, 'P', table.tamano, '+')
                    generator.addExp(paramTemp, paramTemp, '1', '+')
                    generator.setStack(paramTemp, res_left.valor)
                    generator.addExp(paramTemp, paramTemp, '1', '+')
                    generator.setStack(paramTemp, res_right.valor)
                    generator.newEnv(table.tamano)
                    generator.callFun('Pow')
                    paramTemp = generator.addTemp()
                    generator.getStack(paramTemp, 'P')
                    generator.retEnv(table.tamano)
                    return Return(paramTemp, TIPOS.ENTERO, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    generator.fPow()
                    paramTemp = generator.addTemp()
                    generator.addExp(paramTemp, 'P', table.tamano, '+')
                    generator.addExp(paramTemp, paramTemp, '1', '+')
                    generator.setStack(paramTemp, res_left.valor)
                    generator.addExp(paramTemp, paramTemp, '1', '+')
                    generator.setStack(paramTemp, res_right.valor)
                    generator.newEnv(table.tamano)
                    generator.callFun('Pow')
                    paramTemp = generator.addTemp()
                    generator.getStack(paramTemp, 'P')
                    generator.retEnv(table.tamano)
                    return Return(paramTemp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para ^",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    return Primitivo(TIPOS.DECIMAL, float(str(res_left.valor)) ** int(str(res_right.valor)), self.fila, self.columna)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    return Primitivo(TIPOS.DECIMAL, float(str(res_left.valor)) ** float(str(res_right.valor)), self.fila, self.columna)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para ^",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.CADENA):
                if(res_right.tipo==TIPOS.ENTERO):
                    generator.fpowString()
                    paramTemp = generator.addTemp()
                    generator.addExp(paramTemp, 'P', table.tamano, '+')
                    generator.addExp(paramTemp, paramTemp, '1', '+')
                    generator.setStack(paramTemp, res_left.valor)
                    generator.addExp(paramTemp, paramTemp, '1', '+')
                    generator.setStack(paramTemp, res_right.valor)
                    generator.newEnv(table.tamano)
                    generator.callFun('powString')
                    paramTemp = generator.addTemp()
                    generator.getStack(paramTemp, 'P')
                    generator.retEnv(table.tamano)
                    return Return(paramTemp, TIPOS.CADENA, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para ^",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para ^",self.fila,self.columna)
        
        elif (self.operador==OperadorAritmetico.MOD):
            op='%'
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    generator.addMod(temp, res_left.valor,res_right.valor)
                    return Return(temp, TIPOS.ENTERO, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    generator.addMod(temp, res_left.valor,res_right.valor)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para %",self.fila,self.columna)
            elif (res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    generator.addMod(temp, res_left.valor,res_right.valor)
                    return Return(temp, TIPOS.DECIMAL, True)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    generator.addMod(temp, res_left.valor,res_right.valor)
                    return Return(temp, TIPOS.DECIMAL, True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para %",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para %",self.fila,self.columna)
        
        elif (self.operador==OperadorAritmetico.UNMENOS):
            op='*'
            if(res_uni.tipo==TIPOS.ENTERO):
                generator.addExp(temp, res_uni.valor,-1,op)
                return Return(temp, TIPOS.ENTERO, True)
            elif(res_uni.tipo==TIPOS.DECIMAL):
                generator.addExp(temp, res_uni.valor,-1,op)
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