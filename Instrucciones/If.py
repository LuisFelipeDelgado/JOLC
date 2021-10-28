from Instrucciones.Continue import Continue
from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from Instrucciones.Return import ReturnI
from Excepciones.Excepcion import Excepcion
from TS.TCI import TCI
from TS.Tipo import TIPOS
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break

class If(Expresion):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, fila, columna, salidaE=None):
        self.condicion = condicion
        self.listainstrucciones = instruccionesIf
        self.listainstrucciones2 = instruccionesElse
        self.fila = fila
        self.columna = columna
        self.salida=salidaE

    def interpretar(self, tree, table):
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        codigoR.addComment("Compilacion de If")
        condicion = self.condicion.interpretar(tree, table)
        if isinstance(condicion, Excepcion): return condicion

        if condicion.tipo == TIPOS.BOOLEANO:
            codigoR.putE(condicion.ev)
            if self.listainstrucciones2 is not None:
                if isinstance(self.listainstrucciones2, list):
                    for instruccion in self.listainstrucciones:
                        result = instruccion.interpretar(tree, table) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if result is not None : return result
                    if self.salida is None:
                        salidaIf = codigoR.newE()
                    else:
                        salidaIf = self.salida
                    codigoR.GoTo(salidaIf)
                    codigoR.putE(condicion.ef)
                    for instruccion in self.listainstrucciones2:
                        result = instruccion.interpretar(tree, table) #EJECUTA INSTRUCCION ADENTRO DEL ELSE
                        if result is not None : return result
                    codigoR.putE(salidaIf)

                elif isinstance(self.listainstrucciones2, If):
                    for instruccion in self.listainstrucciones:
                        result = instruccion.interpretar(tree, table) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if result is not None : return result
                    if self.salida is None:
                        salidaIf = codigoR.newE()
                    else:
                        salidaIf = self.salida
                    codigoR.GoTo(salidaIf)
                    codigoR.putE(condicion.ef)
                    self.listainstrucciones2.salida=salidaIf
                    self.listainstrucciones2.interpretar(tree, table)
            else:
                for instruccion in self.listainstrucciones:
                    result = instruccion.interpretar(tree, table) #EJECUTA INSTRUCCION ADENTRO DEL IF
                if self.salida is None:
                    codigoR.putE(condicion.ef)
                else:
                    salidaIf = self.salida
                    codigoR.putE(condicion.ef)
                    codigoR.putE(salidaIf)

        else:
            return Excepcion("Semantico", "Tipo de dato no booleano en IF.", self.fila, self.columna)


    def getNodo(self):
        nodo1 = NodoAST("IF")
        nodo1.agregarHijo("if")
        nodoc = NodoAST("CONDICION")
        nodoc.agregarHijoNodo(self.condicion.getNodo())
        nodo1.agregarHijoNodo(nodoc)
        instruccioness2 = NodoAST("INSTRUCCIONES")
        for i in self.listainstrucciones:
            if i == self.listainstrucciones[0]:
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
        if self.listainstrucciones2 is not None:
            if isinstance(self.listainstrucciones2,list):
                nodo1.agregarHijo("else")
                instruccioness2 = NodoAST("INSTRUCCIONES")
                for i in self.listainstrucciones2:
                    if i == self.listainstrucciones2[0]:
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
            else:
                nodo1.agregarHijo("elseif")
                nodo1.agregarHijoNodo(self.listainstrucciones2.getNodo())
        else:
            nodo1.agregarHijo("end")
            nodo1.agregarHijo(";")
        return nodo1
    