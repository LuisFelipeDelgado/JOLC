from Instrucciones.Continue import Continue
from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from Instrucciones.Return import Return
from Excepciones.Excepcion import Excepcion
from TS.Tipo import TIPOS
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class If(Expresion):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, fila, columna):
        self.condicion = condicion
        self.listainstrucciones = instruccionesIf
        self.listainstrucciones2 = instruccionesElse
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        condicion = self.condicion.interpretar(tree, table)
        if isinstance(condicion, Excepcion): return condicion

        if condicion.tipo == TIPOS.BOOLEANO:
            if self.listainstrucciones2 is not None:
                if isinstance(self.listainstrucciones2, list):
                    if bool(condicion.valor) == True:
                        for instruccion in self.listainstrucciones:
                            result = instruccion.interpretar(tree, table) #EJECUTA INSTRUCCION ADENTRO DEL IF
                            if isinstance(result, Excepcion) : return result
                            elif isinstance(result, Break): return result
                            elif isinstance(result, Return): return result
                        return True
                    else:   # VERIFICA SI ES VERDADERA LA CONDICION
                        for instruccion in self.listainstrucciones2:
                            result = instruccion.interpretar(tree, table) #EJECUTA INSTRUCCION ADENTRO DEL ELSE
                            if isinstance(result, Excepcion) : tree.updateConsola(result.toString())
                            elif isinstance(result, Break): return result
                            elif isinstance(result, Return): return result
                        return False
                
                elif isinstance(self.listainstrucciones2, If):
                    if bool(condicion.valor) == True:
                        for instruccion in self.listainstrucciones:
                            result = instruccion.interpretar(tree, table) #EJECUTA INSTRUCCION ADENTRO DEL IF
                            if isinstance(result, Excepcion) : return result
                            elif isinstance(result, Break): return result
                            elif isinstance(result, Continue): return result
                            elif isinstance(result, Return): return result
                    else:               #ELSE
                        return self.listainstrucciones2.interpretar(tree, table)
            else:
                if bool(condicion.valor) == True:
                    for instruccion in self.listainstrucciones:
                        result = instruccion.interpretar(tree, table) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) : return result
                        elif isinstance(result, Break): return result
                        elif isinstance(result, Continue): return result
                        elif isinstance(result, Return): return result
                    return True
                else:               #ELSE
                    return False

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
    