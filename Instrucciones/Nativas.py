from Abstract.ReturnA import Return
from Expresiones.Primitivo import Primitivo
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Expresion
from Excepciones.Excepcion import Excepcion
from TS.TCI import TCI
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
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        if(self.funcion==FuncionNativa.PARSE):
            if(res_left.tipo==TIPOS.CADENA):
                if(self.operacion2.tipos==TIPOS.ENTERO):
                    tempP=codigoR.addTemp()
                    tempP2=codigoR.addTemp()
                    tempP3=codigoR.addTemp()
                    tempP4=codigoR.addTemp()
                    tempP5=codigoR.addTemp()
                    codigoR.addExp(tempP,res_left.valor,'','')
                    codigoR.addExp(tempP3,'0','','')
                    compE=codigoR.newE()
                    avanE=codigoR.newE()
                    salidaE=codigoR.newE()
                    codigoR.putE(compE)
                    codigoR.getHeap(tempP2,tempP)
                    codigoR.addIf(tempP2,'-1','!=',avanE)
                    codigoR.GoTo(salidaE)
                    codigoR.putE(avanE)
                    codigoR.addExp(tempP,tempP,'1','+')
                    codigoR.addExp(tempP3,tempP3,'1','+')
                    codigoR.GoTo(compE)
                    codigoR.putE(salidaE)

                    compE=codigoR.newE()
                    avanE=codigoR.newE()
                    salidaE=codigoR.newE()
                    codigoR.addExp(tempP4,'1','','')
                    codigoR.putE(compE)
                    codigoR.addIf(tempP3,'2','>=',avanE)
                    codigoR.GoTo(salidaE)
                    codigoR.putE(avanE)
                    codigoR.addExp(tempP4,tempP4,'10','*')
                    codigoR.addExp(tempP3,tempP3,'1','-')
                    codigoR.GoTo(compE)
                    codigoR.putE(salidaE)

                    compE=codigoR.newE()
                    avanE=codigoR.newE()
                    salidaE=codigoR.newE()
                    codigoR.addExp(tempP,res_left.valor,'','')
                    codigoR.addExp(tempP5,'0','','')
                    codigoR.putE(compE)
                    codigoR.getHeap(tempP2,tempP)
                    codigoR.addIf(tempP2,'-1','!=',avanE)
                    codigoR.GoTo(salidaE)
                    codigoR.putE(avanE)
                    codigoR.addExp(tempP2,tempP2,'48','-')
                    codigoR.addExp(tempP2,tempP2,tempP4,'*')
                    codigoR.addExp(tempP5,tempP5,tempP2,'+')
                    codigoR.addExp(tempP4,tempP4,'10','/')
                    codigoR.addExp(tempP,tempP,'1','+')
                    codigoR.GoTo(compE)
                    codigoR.putE(salidaE)
                    return Return(tempP5,TIPOS.ENTERO,True)
                elif(self.operacion2.tipos==TIPOS.DECIMAL):
                    tempP=codigoR.addTemp()
                    tempP2=codigoR.addTemp()
                    tempP3=codigoR.addTemp()
                    tempP4=codigoR.addTemp()
                    tempP5=codigoR.addTemp()
                    codigoR.addExp(tempP,res_left.valor,'','')
                    codigoR.addExp(tempP3,'0','','')
                    compE=codigoR.newE()
                    avanE=codigoR.newE()
                    salidaE=codigoR.newE()
                    codigoR.putE(compE)
                    codigoR.getHeap(tempP2,tempP)
                    codigoR.addIf(tempP2,'46','!=',avanE)
                    codigoR.GoTo(salidaE)
                    codigoR.putE(avanE)
                    codigoR.addExp(tempP,tempP,'1','+')
                    codigoR.addExp(tempP3,tempP3,'1','+')
                    codigoR.GoTo(compE)
                    codigoR.putE(salidaE)

                    compE=codigoR.newE()
                    avanE=codigoR.newE()
                    salidaE=codigoR.newE()
                    codigoR.addExp(tempP4,'1','','')
                    codigoR.putE(compE)
                    codigoR.addIf(tempP3,'2','>=',avanE)
                    codigoR.GoTo(salidaE)
                    codigoR.putE(avanE)
                    codigoR.addExp(tempP4,tempP4,'10','*')
                    codigoR.addExp(tempP3,tempP3,'1','-')
                    codigoR.GoTo(compE)
                    codigoR.putE(salidaE)

                    compE=codigoR.newE()
                    avanE=codigoR.newE()
                    salidaE=codigoR.newE()
                    codigoR.addExp(tempP,res_left.valor,'','')
                    codigoR.addExp(tempP5,'0','','')
                    codigoR.putE(compE)
                    codigoR.getHeap(tempP2,tempP)
                    codigoR.addIf(tempP2,'-1','!=',avanE)
                    codigoR.GoTo(salidaE)
                    codigoR.putE(avanE)
                    codigoR.addExp(tempP,tempP,'1','+')
                    codigoR.addIf(tempP2,'46','==',compE)
                    codigoR.addExp(tempP2,tempP2,'48','-')
                    codigoR.addExp(tempP2,tempP2,tempP4,'*')
                    codigoR.addExp(tempP5,tempP5,tempP2,'+')
                    codigoR.addExp(tempP4,tempP4,'10','/')
                    codigoR.GoTo(compE)
                    codigoR.putE(salidaE)
                    return Return(tempP5,TIPOS.DECIMAL,True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para parse",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para parse",self.fila,self.columna)
        elif(self.funcion==FuncionNativa.TRUNC):
            if(res_left.tipo==TIPOS.DECIMAL):
                if (self.operacion2.tipos==TIPOS.ENTERO):
                    tempP = codigoR.addTemp()
                    codigoR.addExp(tempP,res_left.valor,'','')
                    tempP2 = codigoR.addTemp()
                    codigoR.addTrunc(tempP2,tempP)
                    return Return(tempP2,TIPOS.ENTERO,True)
                else:
                    return Excepcion("Semantico", "Tipo erroneo para trunc",self.fila,self.columna)
            else:
                return Excepcion("Semantico", "Tipo erroneo para trunc",self.fila,self.columna)
        elif(self.funcion==FuncionNativa.FLOAT):
            if(res_uni.tipo==TIPOS.ENTERO):
                tempP = codigoR.addTemp()
                codigoR.addExp(tempP,res_uni.valor,'','')
                tempP2 = codigoR.addTemp()
                codigoR.addTrunc(tempP2,tempP)
                return Return(tempP2,TIPOS.DECIMAL,True)
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
        elif(self.funcion==FuncionNativa.LENGTH):
            if(res_uni.tipo==TIPOS.ARREGLO):
                tempP=codigoR.addTemp()
                codigoR.getHeap(tempP,res_uni.valor)
                return Return(tempP,TIPOS.ENTERO,True)
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
    LENGTH = 5