from Expresiones.Primitivo import Primitivo
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Expresion
from Excepciones.Excepcion import Excepcion
from TS.Tipo import TIPOS
from enum import Enum
import math

class ENativas(Expresion):
    def __init__(self, funcion, operacion, fila, columna, operacion2=None):
        self.tipo = TIPOS.CADENA
        self.funcion = funcion
        self.operacion1 = operacion
        self.fila = fila
        self.columna = columna
        self.operacion2 = operacion2

    def interpretar(self, tree, table):
        res_left = None
        res_right = None
        res_uni = None
        if self.operacion2 != None:
            res_left = self.operacion1.interpretar(tree, table)
            res_right = self.operacion2.interpretar(tree,table)
            if isinstance(res_left, Excepcion):
                return res_left
            if isinstance(res_right, Excepcion):
                return res_right;  
        else:
            res_uni = self.operacion1.interpretar(tree, table)
            if isinstance(res_uni, Excepcion):
                return res_uni
        if(self.funcion==ExpresionNativa.LOG):
            if(res_left.tipo==TIPOS.ENTERO):
                if(res_right.tipo==TIPOS.ENTERO):
                    return Primitivo(TIPOS.DECIMAL, math.log(int(str(res_right.valor)),int(str(res_left.valor))), self.fila, self.columna)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    return Primitivo(TIPOS.DECIMAL, math.log(float(str(res_right.valor)),int(str(res_left.valor))), self.fila, self.columna)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para log",self.fila,self.columna)
            elif(res_left.tipo==TIPOS.DECIMAL):
                if(res_right.tipo==TIPOS.ENTERO):
                    return Primitivo(TIPOS.DECIMAL, math.log(int(str(res_right.valor)),float(str(res_left.valor))), self.fila, self.columna)
                elif(res_right.tipo==TIPOS.DECIMAL):
                    return Primitivo(TIPOS.DECIMAL, math.log(float(str(res_right.valor)),float(str(res_left.valor))), self.fila, self.columna)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para log",self.fila,self.columna)
        elif(self.funcion==ExpresionNativa.LOG10):
            if(res_uni.tipo==TIPOS.ENTERO):
                return Primitivo(TIPOS.DECIMAL, math.log(int(str(res_uni.valor)),10), self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.DECIMAL):
                return Primitivo(TIPOS.DECIMAL, math.log(int(str(res_uni.valor)),10), self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para log10",self.fila,self.columna)
        elif(self.funcion==ExpresionNativa.SIN):
            if(res_uni.tipo==TIPOS.ENTERO):
                return Primitivo(TIPOS.DECIMAL, math.sin(int(str(res_uni.valor))), self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.DECIMAL):
                return Primitivo(TIPOS.DECIMAL, math.sin(float(str(res_uni.valor))), self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para sin",self.fila,self.columna)
        elif(self.funcion==ExpresionNativa.COS):
            if(res_uni.tipo==TIPOS.ENTERO):
                return Primitivo(TIPOS.DECIMAL, math.cos(int(str(res_uni.valor))), self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.DECIMAL):
                return Primitivo(TIPOS.DECIMAL, math.cos(float(str(res_uni.valor))), self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para cos",self.fila,self.columna)
        elif(self.funcion==ExpresionNativa.TAN):
            if(res_uni.tipo==TIPOS.ENTERO):
                return Primitivo(TIPOS.DECIMAL, math.tan(int(str(res_uni.valor))), self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.DECIMAL):
                return Primitivo(TIPOS.DECIMAL, math.tan(float(str(res_uni.valor))), self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para tan",self.fila,self.columna)
        elif(self.funcion==ExpresionNativa.SQRT):
            if(res_uni.tipo==TIPOS.ENTERO):
                return Primitivo(TIPOS.DECIMAL, math.sqrt(int(str(res_uni.valor))), self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.DECIMAL):
                return Primitivo(TIPOS.DECIMAL, math.sqrt(float(str(res_uni.valor))), self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para tan",self.fila,self.columna)
        return Excepcion("Semantico", "Operador desconocido",self.fila,self.columna)

    def getNodo(self):
        nodo = NodoAST("NATIVAS")
        if self.operacion2 != None:
            op = self.returnTipo()
            nodo.agregarHijo(op)
            nodo.agregarHijo("(")
            nodo.agregarHijoNodo(self.operacion1.getNodo())
            nodo.agregarHijo(",")
            nodo.agregarHijoNodo(self.operacion2.getNodo())
            nodo.agregarHijo(")")
        else:
            op = self.returnTipo()
            nodo.agregarHijo(op)
            nodo.agregarHijo("(")
            nodo.agregarHijoNodo(self.operacion1.getNodo())
            nodo.agregarHijo(")")
        
        return nodo

    def returnTipo(self):
        ret=""
        if self.funcion==ExpresionNativa.LOG:
            ret="LOG"
        elif self.funcion==ExpresionNativa.LOG10:
            ret="LOG10"
        elif self.funcion==ExpresionNativa.SIN:
            ret="SIN"
        elif self.funcion==ExpresionNativa.COS:
            ret="COS"
        elif self.funcion==ExpresionNativa.TAN:
            ret="TAN"
        elif self.funcion==ExpresionNativa.SQRT:
            ret="SQRT"
        return ret
    
class ExpresionNativa(Enum):
    LOG = 1
    LOG10 = 2
    SIN = 3
    COS = 4
    TAN = 5
    SQRT = 6