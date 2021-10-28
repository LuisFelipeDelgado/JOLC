from TS.Simbolo import Simbolo
from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPOS
from Instrucciones.Return import ReturnI
from Excepciones.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from TS.TCI import TCI


class Funcion(Expresion):
    def __init__(self, nombre, tipo, parametros, instrucciones, fila, columna):
        self.nombre = nombre
        self.tipos=None
        self.tipo=None
        if isinstance(tipo,list):
            self.tipo=TIPOS.ARREGLO
            self.tipos=tipo
        elif tipo is not None:
            self.tipo=tipo
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table):
        table.setFuncion(self.nombre, self)
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        
        nuevaTabla = TablaSimbolos(table)

        returnE = codigoR.newE()
        nuevaTabla.returnE = returnE
        nuevaTabla.tamano = 1

        for param in self.parametros:
            simbolo = Simbolo(param.tipo, param.nombre, self.fila,self.columna,param.tipos,nuevaTabla.tamano,False, ((param.tipo == TIPOS.CADENA) | (param.tipo == TIPOS.STRUCT) | (param.tipo == TIPOS.ARREGLO)))
            porsi = nuevaTabla.actualizarTabla(simbolo)
        
        codigoR.addBeginFunc(self.nombre)

        for instr in self.instrucciones:
            instr.interpretar(tree,nuevaTabla)
        
        codigoR.putE(returnE)
        codigoR.addEndFunc()

    def getNodo(self):
        nodo1 = NodoAST("FUNCION")
        nodo1.agregarHijo(str(self.nombre))
        nodo1.agregarHijo("(")
        if len(self.parametros)>0:
            nodo = NodoAST("PARAMETROS")
            for i in self.parametros:
                if i == self.parametros[0]:
                    instruccioness3 = NodoAST("PARAMETRO")
                    instruccioness3.agregarHijo(i)
                    nodo.agregarHijoNodo(instruccioness3)
                else:
                    instrtmp = nodo
                    instruccioness3 = NodoAST("PARAMETRO")
                    nodo = NodoAST("PARAMETROS")
                    nodo.agregarHijoNodo(instrtmp)
                    nodo.agregarHijo(",")
                    instruccioness3.agregarHijo(i)
                    nodo.agregarHijoNodo(instruccioness3)
            nodo1.agregarHijoNodo(nodo)
        nodo1.agregarHijo(")")
        instruccioness2 = NodoAST("INSTRUCCIONES")
        if None in self.instrucciones:
            self.instrucciones.remove(None)
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