from Expresiones.Primitivo import Primitivo
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Expresion
from Excepciones.Excepcion import Excepcion
from TS.Tipo import TIPO, TIPOS
from enum import Enum
from math import trunc

class FNativas(Expresion):
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
            if isinstance(res_left, Excepcion):
                return res_left
            if not isinstance(self.operacion2,TIPO):
                res_right = self.operacion2.interpretar(tree, table)
                if isinstance(res_right, Excepcion):
                    return res_right
        else:
            res_uni = self.operacion1.interpretar(tree, table)
            if isinstance(res_uni, Excepcion):
                return res_uni
        if(self.funcion==FuncionNativa.PARSE):
            if(res_left.tipo==TIPOS.CADENA):
                if(self.operacion2.tipos==TIPOS.ENTERO):
                    return Primitivo(TIPOS.ENTERO, int(trunc(float(str(res_left.valor)))), self.fila, self.columna)
                elif(self.operacion2.tipos==TIPOS.DECIMAL):
                    return Primitivo(TIPOS.DECIMAL, float(str(res_left.valor)), self.fila, self.columna)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para parse",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para parse",self.fila,self.columna)
        elif(self.funcion==FuncionNativa.TRUNC):
            if(res_left.tipo==TIPOS.DECIMAL):
                if (self.operacion2.tipos==TIPOS.ENTERO):
                    return Primitivo(TIPOS.ENTERO, int(trunc(float(str(res_left.valor)))), self.fila, self.columna)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para trunc",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para trunc",self.fila,self.columna)
        elif(self.funcion==FuncionNativa.FLOAT):
            if(res_uni.tipo==TIPOS.ENTERO):
                return Primitivo(TIPOS.DECIMAL, float(str(res_uni.valor)), self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para float",self.fila,self.columna)
        elif(self.funcion==FuncionNativa.STRING):
            if(res_uni.tipo==TIPOS.ENTERO):
                return Primitivo(TIPOS.CADENA, str(res_uni.valor), self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.DECIMAL):
                return Primitivo(TIPOS.CADENA, str(res_uni.valor), self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.BOOLEANO):
                return Primitivo(TIPOS.CADENA, str(res_uni.valor), self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.CHARACTER):
                return Primitivo(TIPOS.CADENA, str(res_uni.valor), self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.CADENA):
                return Primitivo(TIPOS.CADENA, str(res_uni.valor), self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para string",self.fila,self.columna)
        elif(self.funcion==FuncionNativa.TYPEOF):
            if(res_uni.tipo==TIPOS.ENTERO):
                return Primitivo(TIPOS.CADENA, "Int64", self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.DECIMAL):
                return Primitivo(TIPOS.CADENA, "Float64", self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.BOOLEANO):
                return Primitivo(TIPOS.CADENA, "Bool", self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.CHARACTER):
                return Primitivo(TIPOS.CADENA, "Char", self.fila, self.columna)
            elif(res_uni.tipo==TIPOS.CADENA):
                return Primitivo(TIPOS.CADENA, "String", self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para Typeof",self.fila,self.columna)
        elif(self.funcion==FuncionNativa.UPPERCASE):
            if(res_uni.tipo==TIPOS.CADENA):
                return Primitivo(TIPOS.CADENA, str(res_uni.valor).upper(), self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para uppercase",self.fila,self.columna)
        elif(self.funcion==FuncionNativa.LOWERCASE):
            if(res_uni.tipo==TIPOS.CADENA):
                return Primitivo(TIPOS.CADENA, str(res_uni.valor).lower(), self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para lowercase",self.fila,self.columna)
        elif(self.funcion==FuncionNativa.PUSH):
            if(res_left.tipo==TIPOS.ARREGLO):
                res_left.valor.append(res_right)
                return None
            else:
                return Excepcion("Semantico", "Tipo erroneo para push",self.fila,self.columna)
        elif(self.funcion==FuncionNativa.POP):
            if(res_uni.tipo==TIPOS.ARREGLO):
                res = res_uni.valor.pop()
                res.fila=self.fila
                res.columna=self.columna
                return res
            else:
                return Excepcion("Semantico", "Tipo erroneo para pop",self.fila,self.columna)
        elif(self.funcion==FuncionNativa.LENGTH):
            if(res_uni.tipo==TIPOS.ARREGLO):
                return Primitivo(TIPOS.ENTERO, len(res_uni.valor), self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para length",self.fila,self.columna)
        return Excepcion("Semantico", "Operador desconocido",self.fila,self.columna)

    def getNodo(self):
        nodo = NodoAST("NATIVAS")
        if self.operacion2 != None:
            op = self.returnTipo()
            nodo.agregarHijo(op)
            nodo.agregarHijo("(")
            nodo.agregarHijoNodo(self.operacion1.getNodo())
            nodo.agregarHijo(",")
            if not isinstance(self.operacion2,TIPO):
                nodo.agregarHijoNodo(self.operacion2.getNodo())
            else:
                nodo.agregarHijo(self.operacion2.tipos.name)
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
        if self.funcion==FuncionNativa.PARSE:
            ret="PARSE"
        elif self.funcion==FuncionNativa.TRUNC:
            ret="TRUNC"
        elif self.funcion==FuncionNativa.FLOAT:
            ret="FLOAT"
        elif self.funcion==FuncionNativa.STRING:
            ret="STRING"
        elif self.funcion==FuncionNativa.TYPEOF:
            ret="TYPEOF"
        elif self.funcion==FuncionNativa.PUSH:
            ret="PUSH!"
        elif self.funcion==FuncionNativa.POP:
            ret="POP!"
        elif self.funcion==FuncionNativa.LENGTH:
            ret="LENGTH"
        elif self.funcion==FuncionNativa.LOWERCASE:
            ret="LOWERCASE"
        elif self.funcion==FuncionNativa.UPPERCASE:
            ret="UPPERCASE"
        return ret
    
class FuncionNativa(Enum):
    PARSE = 1
    TRUNC = 2
    FLOAT = 3
    STRING = 4
    TYPEOF = 5
    PUSH = 6
    POP = 7
    LENGTH = 8
    LOWERCASE = 9
    UPPERCASE = 10