from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from TS.TCI import TCI
from TS.Tipo import TIPOS
from TS.TablaSimbolos import TablaSimbolos

class ReturnI(Expresion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()
        if self.expresion is not None:
            value = self.expresion.interpretar(tree,table)
            if(value.tipo == TIPOS.BOOLEANO):
                tempE = codigoR.newE()
                
                codigoR.putE(value.ev)
                codigoR.setStack('P', '1')
                codigoR.GoTo(tempE)

                codigoR.putE(value.ef)
                codigoR.setStack('P', '0')

                codigoR.putE(tempE)
            else:
                codigoR.setStack('P', value.valor)
            
        codigoR.GoTo(table.returnE)

    def getNodo(self):
        nodo = NodoAST("RETURN")
        nodo.agregarHijo("return")
        if self.expresion!= None:
            nodo.agregarHijoNodo(self.expresion.getNodo())
        nodo.agregarHijo(";")
        return nodo