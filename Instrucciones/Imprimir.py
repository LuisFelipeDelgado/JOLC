import copy
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
                    tempE = codigoR.newE()
                    codigoR.putE(val.ev)
                    codigoR.printTrue()
                    codigoR.GoTo(tempE)
                    codigoR.putE(val.ef)
                    codigoR.printFalse()
                    codigoR.putE(tempE)
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
                elif val.tipo == TIPOS.ARREGLO:
                    codigoR.addPrint('c','91')

                    tempP = codigoR.addTemp()
                    tempP3 = codigoR.addTemp()
                    tempP4 = codigoR.addTemp()
                    continueE = codigoR.newE()
                    entradaE = codigoR.newE()
                    salidaE = codigoR.newE()
                    condicionE = codigoR.newE()
                    codigoR.getHeap(tempP3,val.valor)
                    codigoR.addExp(val.valor,val.valor,'1','+')
                    codigoR.getHeap(tempP4,val.valor)
        
                    codigoR.putE(continueE)
                    codigoR.addIf(tempP3,'0','!=',entradaE)
                    codigoR.GoTo(salidaE)
                    codigoR.putE(entradaE)
                    
                    if val.aux[0] == TIPOS.DECIMAL:
                        codigoR.addPrint('f',tempP4)
                    elif val.aux[0] == TIPOS.ENTERO:
                        codigoR.addPrint('d',tempP4)
                    elif val.aux[0] == TIPOS.CADENA:
                        codigoR.fPrintString()

                        paramTemp = codigoR.addTemp()
                        
                        codigoR.addExp(paramTemp, 'P', table.tamano, '+')
                        codigoR.addExp(paramTemp, paramTemp, '1', '+')
                        codigoR.setStack(paramTemp, tempP4)
                        
                        codigoR.newEnv(table.tamano)
                        codigoR.callFun('printString')

                        temp = codigoR.addTemp()
                        codigoR.getStack(temp, 'P')
                        codigoR.retEnv(table.tamano)
                    elif val.aux[0] == TIPOS.ARREGLO:
                        aux2 = copy.deepcopy(val.aux)
                        aux2.pop(0)
                        self.print_arreglo(aux2,tempP4,table)

                    codigoR.addPrint('c','44')
                    codigoR.GoTo(condicionE)
                    codigoR.putE(condicionE)
                    codigoR.addExp(tempP3,tempP3,'1','-')
                    codigoR.addExp(val.valor,val.valor,'1','+')
                    codigoR.getHeap(tempP4,val.valor)
                    codigoR.setStack(tempP,tempP4)
                    codigoR.GoTo(continueE)
                    codigoR.putE(salidaE)
                    codigoR.addPrint('c','93')
                    '''valor1 = m.interpretar(tree,table)
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
    
    def print_arreglo(self,aux,val,table):
                    codigoAux = TCI()
                    codigoR = codigoAux.getInstance()
                    codigoR.addPrint('c','91')

                    tempP = codigoR.addTemp()
                    tempP3 = codigoR.addTemp()
                    tempP4 = codigoR.addTemp()
                    continueE = codigoR.newE()
                    entradaE = codigoR.newE()
                    salidaE = codigoR.newE()
                    condicionE = codigoR.newE()
                    codigoR.getHeap(tempP3,val)
                    codigoR.addExp(val,val,'1','+')
                    codigoR.getHeap(tempP4,val)
        
                    codigoR.putE(continueE)
                    codigoR.addIf(tempP3,'0','!=',entradaE)
                    codigoR.GoTo(salidaE)
                    codigoR.putE(entradaE)
                    
                    if aux[0] == TIPOS.DECIMAL:
                        codigoR.addPrint('f',tempP4)
                    elif aux[0] == TIPOS.ENTERO:
                        codigoR.addPrint('d',tempP4)
                    elif aux[0] == TIPOS.CADENA:
                        codigoR.fPrintString()

                        paramTemp = codigoR.addTemp()
                        
                        codigoR.addExp(paramTemp, 'P', table.tamano, '+')
                        codigoR.addExp(paramTemp, paramTemp, '1', '+')
                        codigoR.setStack(paramTemp, tempP4)
                        
                        codigoR.newEnv(table.tamano)
                        codigoR.callFun('printString')

                        temp = codigoR.addTemp()
                        codigoR.getStack(temp, 'P')
                        codigoR.retEnv(table.tamano)
                    elif aux[0] == TIPOS.ARREGLO:
                        aux2 = copy.deepcopy(aux)
                        aux2.pop(0)
                        self.print_arreglo(aux2,tempP4,table)

                    codigoR.addPrint('c','44')
                    codigoR.GoTo(condicionE)
                    codigoR.putE(condicionE)
                    codigoR.addExp(tempP3,tempP3,'1','-')
                    codigoR.addExp(val,val,'1','+')
                    codigoR.getHeap(tempP4,val)
                    codigoR.setStack(tempP,tempP4)
                    codigoR.GoTo(continueE)
                    codigoR.putE(salidaE)
                    codigoR.addPrint('c','93')
    
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
    