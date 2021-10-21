from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from TS.TCI import TCI
from TS.Tipo import TIPOS

class Imprimir(Expresion):
    def __init__(self, expresion, fila, columna, opcion):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.opcion = opcion

    def interpretar(self, tree, table):
        valor1 = None
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        if self.expresion!=None:
            for m in self.expresion:
                val = m.interpretar(tree,table)
                if val.tipo == TIPOS.ENTERO:
                    codigoR.addPrint("d",val.valor)
                elif val.tipo == TIPOS.DECIMAL:
                    codigoR.addPrint("f",val.valor)
                elif val.tipo == TIPOS.BOOLEANO:
                    tempLbl = codigoR.newE()
                    codigoR.putE(val.ev)
                    codigoR.printTrue()
                    codigoR.GoTo(tempLbl)
                    codigoR.putE(val.ef)
                    codigoR.printFalse()
                    codigoR.putE(tempLbl)
                elif val.tipo == TIPOS.CADENA:
                    codigoR.fPrintString()

                    paramTemp = codigoR.addTemp()
                    
                    codigoR.addExp(paramTemp, 'P', table.tamano, '+')
                    codigoR.addExp(paramTemp, paramTemp, '1', '+')
                    codigoR.setStack(paramTemp, val.valor)
                    
                    codigoR.newEnv(table.tamano)
                    codigoR.callFun('printString')

                    temp = codigoR.addTemp()
                    codigoR.getStack(temp, 'P')
                    codigoR.retEnv(table.tamano)
                '''elif val.tipo == TIPOS.ARREGLO:

                valor1 = m.interpretar(tree,table)
                if isinstance(valor1, Excepcion):
                    return valor1
                if not isinstance(valor1,dict):
                    if  valor1.tipo==TIPOS.ARREGLO:
                        val += "["
                        for i in valor1.valor:
                            tmp = i.interpretar(tree,table)
                            if  tmp.tipo==TIPOS.ARREGLO:
                                val += self.print_arreglo(tmp.valor,tree,table)
                            else:
                                val += str(tmp.valor)
                            if i != valor1.valor[-1]:
                                val += ","
                        val += "]"
                    else:
                        val += str(valor1.valor)
                else:
                    val += "{"
                    for i in valor1['atributos']:
                        if isinstance(valor1['atributos'][i],dict):
                            val += self.print_struct(valor1['atributos'][i],tree,table)
                        else:
                            tmp = valor1['atributos'][i].interpretar(tree,table)
                            if  tmp.tipo==TIPOS.ARREGLO:
                                val += self.print_arreglo(tmp.valor,tree,table)
                            else:
                                val += str(tmp.valor)
                            val += ","
                    if val[:-1] !='}':
                        val = val[:-1]
                    val += "}"'''
        if self.opcion == 1:
            codigoR.addPrint("c", 10)
        
    def getNodo(self):
        nodo1 = NodoAST("IMPRIMIR")
        if self.opcion ==1:
            nodo1.agregarHijo("println")
        else:
            nodo1.agregarHijo("print")
        nodo1.agregarHijo("(")
        if self.expresion is not None:
            nodo = NodoAST("varias_coma")
            for i in self.expresion:
                if i == self.expresion[0]:
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
        nodo1.agregarHijo(")")
        nodo1.agregarHijo(";")
        return nodo1
    
    def print_arreglo(self,lista,tree,table):
        val = "["
        for i in lista:
            tmp = i.interpretar(tree,table)
            if  tmp.tipo==TIPOS.ARREGLO:
                val += self.print_arreglo(tmp.valor,tree,table)
            else:
                val += str(tmp.valor)
            if i != lista[-1]:
                val += ","
        val += "]"
        return val
    
    def print_struct(self,valor1,tree,table):
        val = "{"
        for i in valor1['atributos']:
            if isinstance(valor1['atributos'][i],dict):
                val += self.print_struct(valor1['atributos'][i],tree,table)
            else:
                tmp = valor1['atributos'][i].interpretar(tree,table)
                if  tmp.tipo==TIPOS.ARREGLO:
                    val += self.print_arreglo(tmp.valor,tree,table)
                else:
                    val += str(tmp.valor)
                val += ","
        val = val[:-1]
        val += "}"
        return val
    