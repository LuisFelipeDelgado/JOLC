from Abstract.ReturnA import Return
from Abstract.instruccion import Expresion
from Excepciones.Excepcion import Excepcion
from Abstract.NodoAST import NodoAST
from TS.TCI import TCI
from TS.Tipo import TIPOS


class Identificador(Expresion):
    def __init__(self, identificador, fila, columna):
        Expresion.__init__(self,None,fila,columna)
        self.identificador = identificador
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        '''simbolo = table.getVariable(self.identificador)

        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        
        return simbolo.getValor()'''
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()

        codigoR.addComment("Compilacion de Acceso")
        
        var = table.getVariable(self.identificador)
        if(var == None):
            print("Error, no existe la variable")
            return

        # Temporal para guardar variable
        temp = codigoR.addTemp()

        # Obtencion de posicion de la variable
        tempP = var.posicion
        if(not var.globalV):
            tempP = codigoR.addTemp()
            codigoR.addExp(tempP, 'P', var.posicion, "+")
        codigoR.getStack(temp, tempP)

        if var.tipo != TIPOS.BOOLEANO:
            codigoR.addComment("Fin compilacion acceso")
            codigoR.addSpace()
            return Return(temp, var.tipo, True,var.valor,var.tipoS)
        if self.ev == '':
            self.ev = codigoR.newE()
        if self.ef == '':
            self.ef = codigoR.newE()
        
        codigoR.addIf(temp, '1', '==', self.ev)
        codigoR.GoTo(self.ef)

        codigoR.addComment("Fin compilacion acceso")
        codigoR.addSpace()

        ret = Return(None, TIPOS.BOOLEANO, False)
        ret.ev = self.ev
        ret.ef = self.ef
        return ret

    def getNodo(self):
        nodo = NodoAST("IDENTIFICADOR")
        nodo.agregarHijo(str(self.identificador))
        return nodo