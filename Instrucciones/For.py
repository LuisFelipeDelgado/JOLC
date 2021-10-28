from typing import NoReturn
from Abstract.instruccion import Expresion
from Instrucciones.Return import ReturnI
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from TS.Tipo import TIPO, TIPOS
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from TS.Simbolo import Simbolo
from TS.TCI import TCI
import copy

class For(Expresion):
    def __init__(self, condicion, expresion1, instrucciones, fila, columna, expresion2=None):
        self.condicion = condicion
        self.expresion1 = expresion1
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.expresion2 = expresion2

    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
        nuevaTabla.entorno = "For"
        if self.expresion2 is not None:
            tmp1p = self.expresion1.interpretar(tree, table)
            tmp1=copy.deepcopy(tmp1p)
            tmp2p = self.expresion2.interpretar(tree, table)
            tmp2=copy.deepcopy(tmp2p)
            declara = Simbolo(tmp1p.tipo, self.condicion, self.fila, self.columna, None,nuevaTabla.tamano,False,False)
            porsi = nuevaTabla.actualizarTabla(declara)
            codigoAux = TCI()
            codigoR = codigoAux.getInstance()
            tempP = codigoR.addTemp()
            continueE = codigoR.newE()
            entradaE = codigoR.newE()
            salidaE = codigoR.newE()
            condicionE = codigoR.newE()
            codigoR.addExp(tempP,'P',porsi.posicion,'+')
            codigoR.setStack(tempP,tmp1.valor)
            
            codigoR.putE(continueE)
            temp1 = codigoR.addTemp()
            codigoR.addExp(temp1,'P',porsi.posicion,'+')
            temp2 = codigoR.addTemp()
            codigoR.getStack(temp2,temp1)     #NUEVO ENTORNO
            nuevaTabla.entorno = "For"
            nuevaTabla.breakE = salidaE
            nuevaTabla.continueE = condicionE
            codigoR.addIf(temp2,tmp2.valor,'<=',entradaE)
            codigoR.GoTo(salidaE)
            codigoR.putE(entradaE)
            for instr in  self.instrucciones:
                instr.interpretar(tree, nuevaTabla)
            codigoR.GoTo(condicionE)
            codigoR.putE(condicionE)
            temp1 = codigoR.addTemp()
            codigoR.addExp(temp1,'P',porsi.posicion,'+')
            temp2 = codigoR.addTemp()
            codigoR.getStack(temp2,temp1)
            temp3 = codigoR.addTemp()
            codigoR.addExp(temp3,temp2,'1','+')
            codigoR.setStack(temp1,temp3)
            codigoR.GoTo(continueE)
            codigoR.putE(salidaE)
        else:
            tmp1p = self.expresion1.interpretar(tree, table)
            tmp1=copy.deepcopy(tmp1p)
            if tmp1p.tipo == TIPOS.CADENA:
                declara = Simbolo(tmp1p.tipo, self.condicion, self.fila, self.columna, NoReturn,nuevaTabla.tamano+1,False,True)
                porsi = nuevaTabla.actualizarTabla(declara)
                nuevaTabla.tamano=nuevaTabla.tamano+1
                codigoAux = TCI()
                codigoR = codigoAux.getInstance()
                tempP = codigoR.addTemp()
                tempP2 = codigoR.addTemp()
                continueE = codigoR.newE()
                entradaE = codigoR.newE()
                salidaE = codigoR.newE()
                condicionE = codigoR.newE()
                codigoR.addExp(tempP,'P',int(porsi.posicion)-1,'+')
                codigoR.setStack(tempP,tmp1.valor)
                temp1 = codigoR.addTemp()
                codigoR.getStack(temp1,tempP) 
                
                codigoR.addExp(tempP2,'H','','')
                tempP3 = codigoR.addTemp()
                codigoR.getHeap(tempP3,temp1)
                codigoR.setHeap('H',tempP3)
                codigoR.addExp('H','H','1','+')
                codigoR.setHeap('H','-1')
                codigoR.addExp('H','H','1','+')
                codigoR.addExp(tempP,'P',porsi.posicion,'+')
                codigoR.setStack(tempP,tempP2)
                
    
                codigoR.putE(continueE)  #NUEVO ENTORNO
                temp2 = codigoR.addTemp()
                codigoR.getHeap(temp2,tempP2)   
                nuevaTabla.entorno = "For"
                nuevaTabla.breakE = salidaE
                nuevaTabla.continueE = condicionE
                codigoR.addIf(temp2,'-1','!=',entradaE)
                codigoR.GoTo(salidaE)
                codigoR.putE(entradaE)
                for instr in  self.instrucciones:
                    instr.interpretar(tree, nuevaTabla)
                codigoR.GoTo(condicionE)
                codigoR.putE(condicionE)
                codigoR.addExp(temp1,temp1,'1','+')
                codigoR.getHeap(tempP3,temp1)
                codigoR.setHeap(tempP2,tempP3)
                codigoR.GoTo(continueE)
                codigoR.putE(salidaE)
            else:
                aux = None
                bas = None
                if tmp1.aux is not None:
                    if len(tmp1.aux) > 1:
                        aux = copy.deepcopy(tmp1.aux)
                        bas = aux.pop(0)
                declara = Simbolo(tmp1.aux[0], self.condicion, self.fila, self.columna, aux,nuevaTabla.tamano,False,True)
                porsi = nuevaTabla.actualizarTabla(declara)
                nuevaTabla.tamano=nuevaTabla.tamano
                codigoAux = TCI()
                codigoR = codigoAux.getInstance()
                tempP = codigoR.addTemp()
                tempP3 = codigoR.addTemp()
                tempP4 = codigoR.addTemp()
                tempP2 = codigoR.addTemp()
                continueE = codigoR.newE()
                entradaE = codigoR.newE()
                salidaE = codigoR.newE()
                condicionE = codigoR.newE()
                codigoR.getHeap(tempP3,tmp1.valor)
                codigoR.addExp(tempP,'P',int(porsi.posicion),'+')
                codigoR.addExp(tmp1.valor,tmp1.valor,'1','+')
                codigoR.getHeap(tempP4,tmp1.valor)
                codigoR.setStack(tempP,tempP4)
    
                codigoR.putE(continueE)
                nuevaTabla.entorno = "For"
                nuevaTabla.breakE = salidaE
                nuevaTabla.continueE = condicionE
                codigoR.addIf(tempP3,'0','!=',entradaE)
                codigoR.GoTo(salidaE)
                codigoR.putE(entradaE)
                for instr in  self.instrucciones:
                    instr.interpretar(tree, nuevaTabla)
                codigoR.GoTo(condicionE)
                codigoR.putE(condicionE)
                codigoR.addExp(tempP3,tempP3,'1','-')
                codigoR.addExp(tmp1.valor,tmp1.valor,'1','+')
                codigoR.getHeap(tempP4,tmp1.valor)
                codigoR.setStack(tempP,tempP4)
                codigoR.GoTo(continueE)
                codigoR.putE(salidaE)

        '''nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
        nuevaTabla.setEntorno("FOR")
        tree.tablas.append(nuevaTabla)
        if self.expresion2 is not None:
            tmp1p = self.expresion1.interpretar(tree, table)
            tmp1=copy.deepcopy(tmp1p)
            tmp2p = self.expresion2.interpretar(tree, table)
            tmp2=copy.deepcopy(tmp2p)
            declara = Simbolo(TIPO(TIPOS.ENTERO), self.condicion, self.fila, self.columna, tmp1)
            porsi = nuevaTabla.actualizarTabla(declara)
            if(tmp1.tipo==TIPOS.ENTERO):
                    for i in range(int(tmp1.valor), (int(tmp2.valor)+1)):
                        nuevaTabla2 = TablaSimbolos(nuevaTabla)       #NUEVO ENTORNO
                        nuevaTabla2.setEntorno("FOR")
                        tree.tablas.append(nuevaTabla2)
                        for instruccion in self.instrucciones:
                            result = instruccion.interpretar(tree, nuevaTabla2) #EJECUTA INSTRUCCION ADENTRO DEL IF
                            if isinstance(result, Excepcion) :
                                tree.getExcepciones().append(result)
                                tree.updateConsola(result.toString())
                            if isinstance(result, Break): return None
                            if isinstance(result, Continue): break
                            if isinstance(result, Return): return result
                        tmp1.valor = tmp1.valor + 1
                        declara = Simbolo(TIPO(TIPOS.ENTERO), self.condicion, self.fila, self.columna, tmp1)
                        porsi = nuevaTabla.actualizarTabla(declara)
            elif(tmp1.tipo==TIPOS.DECIMAL):
                if(tmp2.tipo==TIPOS.ENTERO):
                    for i in range(int(tmp1.valor), (int(tmp2.valor))):
                        nuevaTabla2 = TablaSimbolos(nuevaTabla)       #NUEVO ENTORNO
                        nuevaTabla2.setEntorno("FOR")
                        tree.tablas.append(nuevaTabla2)
                        for instruccion in self.instrucciones:
                            result = instruccion.interpretar(tree, nuevaTabla2) #EJECUTA INSTRUCCION ADENTRO DEL IF
                            if isinstance(result, Excepcion) :
                                tree.getExcepciones().append(result)
                                tree.updateConsola(result.toString())
                            if isinstance(result, Break): return None
                            if isinstance(result, Continue): break
                            if isinstance(result, Return): return result
                        tmp1.valor = tmp1.valor + 1
                        declara = Simbolo(TIPO(TIPOS.ENTERO), self.condicion, self.fila, self.columna, tmp1)
                        porsi = nuevaTabla.actualizarTabla(declara)
                elif(tmp2.tipo==TIPOS.DECIMAL):
                    for i in range(int(tmp1.valor), (int(tmp2.valor)+1)):
                        nuevaTabla2 = TablaSimbolos(nuevaTabla)       #NUEVO ENTORNO
                        nuevaTabla2.setEntorno("FOR")
                        tree.tablas.append(nuevaTabla2)
                        for instruccion in self.instrucciones:
                            result = instruccion.interpretar(tree, nuevaTabla2) #EJECUTA INSTRUCCION ADENTRO DEL IF
                            if isinstance(result, Excepcion) :
                                tree.getExcepciones().append(result)
                                tree.updateConsola(result.toString())
                            if isinstance(result, Break): return None
                            if isinstance(result, Continue): break
                            if isinstance(result, Return): return result
                        tmp1.valor = tmp1.valor + 1
                        declara = Simbolo(TIPO(TIPOS.ENTERO), self.condicion, self.fila, self.columna, tmp1)
                        porsi = nuevaTabla.actualizarTabla(declara)
            else:
                return Excepcion("Semantico", "Tipo erroneo para rango en For.", self.fila, self.columna)
        else:
            tmp1 = self.expresion1.interpretar(tree, table)
            rep = ""
            if (tmp1.tipo==TIPOS.CADENA):
                rep += tmp1.valor
                tmp2 = copy.deepcopy(tmp1)
                for i in rep:
                    nuevaTabla2 = TablaSimbolos(nuevaTabla)       #NUEVO ENTORNO
                    nuevaTabla2.setEntorno("FOR")
                    tree.tablas.append(nuevaTabla2)
                    for instruccion in self.instrucciones:
                        tmp2.tipo=TIPOS.CHARACTER
                        tmp2.valor = i
                        declara = Simbolo(TIPO(TIPOS.CHARACTER), self.condicion, self.fila, self.columna, tmp2)
                        porsi = nuevaTabla.actualizarTabla(declara)
                        result = instruccion.interpretar(tree, nuevaTabla2) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion):
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                        if isinstance(result, Continue): break
                        if isinstance(result, Return): return result
            elif(tmp1.tipo==TIPOS.ARREGLO):
                rep = tmp1.valor
                for i in rep:
                    ip = i.interpretar(tree,table)
                    nuevaTabla2 = TablaSimbolos(nuevaTabla)       #NUEVO ENTORNO
                    nuevaTabla2.setEntorno("FOR")
                    tree.tablas.append(nuevaTabla2)
                    for instruccion in self.instrucciones:
                        declara = Simbolo(ip.tipo, self.condicion, self.fila, self.columna, ip)
                        porsi = nuevaTabla.actualizarTabla(declara)
                        result = instruccion.interpretar(tree, nuevaTabla2) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion):
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                        if isinstance(result, Continue): break
                        if isinstance(result, Return): return result
            else:
                return Excepcion("Semantico", "Tipo de expresion erronea para iterar en For.", self.fila, self.columna)'''
    
    def getNodo(self):
        nodo1 = NodoAST("FOR")
        nodo1.agregarHijo("for")
        nodo2 = NodoAST("IDENTIFICADOR")
        nodo2.agregarHijo(str(self.condicion))
        nodo1.agregarHijoNodo(nodo2)
        nodo1.agregarHijo("in")
        nodoc = NodoAST("EXPRESION")
        nodoc.agregarHijoNodo(self.expresion1.getNodo())
        nodo1.agregarHijoNodo(nodoc)
        if self.expresion2 is not None:
            nodo1.agregarHijo(":")
            nodoc = NodoAST("EXPRESION2")
            nodoc.agregarHijoNodo(self.expresion2.getNodo())
            nodo1.agregarHijoNodo(nodoc)
        instruccioness2 = NodoAST("INSTRUCCIONES")
        for i in self.instrucciones:
            if i == self.instrucciones[0]:
                instruccioness3 = NodoAST("INSTRUCCION")
                instruccioness3.agregarHijoNodo(i.getNodo())
                instruccioness2.agregarHijoNodo(instruccioness3)
            else:
                instrtmp = instruccioness2
                instruccioness3 = NodoAST("INSTRUCCION")
                instruccioness2 = NodoAST("INSTRUCCIONES")
                instruccioness2.agregarHijoNodo(instrtmp)
                instruccioness3.agregarHijoNodo(i.getNodo())
                instruccioness2.agregarHijoNodo(instruccioness3)
        nodo1.agregarHijoNodo(instruccioness2)
        nodo1.agregarHijo("end")
        nodo1.agregarHijo(";")
        return nodo1
    