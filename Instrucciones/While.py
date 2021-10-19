from Abstract.instruccion import Expresion
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from TS.TCI import TCI
from TS.Tipo import TIPOS
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue

class While(Expresion):
    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        continueE = codigoR.newE()
        codigoR.putE(continueE)
        condicion = self.condicion.interpretar(tree, table)
        nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
        nuevaTabla.entorno = "While"
        nuevaTabla.breakE = condicion.ef
        nuevaTabla.continueE = continueE
        codigoR.putE(condicion.ev)
        for instr in  self.instrucciones:
            instr.interpretar(tree, nuevaTabla)
        codigoR.GoTo(continueE)
        codigoR.putE(condicion.ef)

    def getNodo(self):
        nodo1 = NodoAST("WHILE")
        nodo1.agregarHijo("while")
        nodoc = NodoAST("CONDICION")
        nodoc.agregarHijoNodo(self.condicion.getNodo())
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
    