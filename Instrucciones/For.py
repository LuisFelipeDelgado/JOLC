from Abstract.instruccion import Expresion
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from TS.Tipo import TIPO, TIPOS
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from TS.Simbolo import Simbolo
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
                return Excepcion("Semantico", "Tipo de expresion erronea para iterar en For.", self.fila, self.columna)

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
    