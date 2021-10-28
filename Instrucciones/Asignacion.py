from TS.TCI import TCI
from TS.Tipo import TIPOS
from Abstract.NodoAST import NodoAST
from Excepciones.Excepcion import Excepcion
from Abstract.instruccion import Expresion
from TS.Simbolo import Simbolo

class Asignacion(Expresion):
    def __init__(self, identificador, expresion, fila, columna, tipo=None):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = tipo

    def interpretar(self, tree, table):
        codigoAux = TCI()
        codigoR = codigoAux.getInstance()

        if isinstance(self.tipo, Excepcion):
            return self.tipo
        value = self.expresion.interpretar(tree, table)
        isHeap = False
        if (value.tipo == TIPOS.CADENA) | (value.tipo==TIPOS.STRUCT) | (value.tipo==TIPOS.ARREGLO):
            isHeap=True
        if(self.tipo==None):
            if isinstance(value, Excepcion):
                return value
        else:
            value = self.expresion.interpretar(tree, table)
            if isinstance(value, Excepcion):
                return value
            if(value.tipo!=self.tipo):
                return Excepcion("Semantico", "Tipo erroneo para declaracion",self.fila,self.columna)
        if value.tipo==TIPOS.ARREGLO:
            simbolo = Simbolo(value.tipo, self.identificador, self.fila, self.columna, value.aux,table.tamano,table.anterior==None,isHeap)
        else:
            simbolo = Simbolo(value.tipo, self.identificador, self.fila, self.columna, None,table.tamano,table.anterior==None,isHeap)

        result = table.actualizarTabla(simbolo)     # Si no se encuentra el simbolo, lo agrega 
        tempP = result.posicion
        if not result.globalV:
            tempP = codigoR.addTemp()
            codigoR.addExp(tempP,'P',result.posicion,'+')
        if(value.tipo == TIPOS.BOOLEANO):
            tempE = codigoR.newE()
            
            codigoR.putE(value.ev)
            codigoR.setStack(tempP, "1")
            
            codigoR.GoTo(tempE)

            codigoR.putE(value.ef)
            codigoR.setStack(tempP, "0")

            codigoR.putE(tempE)
        else:
            codigoR.setStack(tempP, value.valor)

    def getNodo(self):
        nodo = NodoAST("ASIGNACION")
        nodo2 = NodoAST("IDENTIFICADOR")
        nodo2.agregarHijo(str(self.identificador))
        nodo.agregarHijoNodo(nodo2)
        nodo.agregarHijo("=")
        nodo3 = NodoAST("EXPRESION")
        nodo3.agregarHijoNodo(self.expresion.getNodo())
        nodo.agregarHijoNodo(nodo3)
        if self.tipo is not None:
            nodo.agregarHijo("::")
            nodo2 = NodoAST("TIPO")
            tmp = self.returnTipo()
            nodo2.agregarHijo(tmp)
            nodo.agregarHijoNodo(nodo2)
        nodo.agregarHijo(";")
        return nodo

    def returnTipo(self):
        ret=""
        if self.tipo==TIPOS.CADENA:
            ret="String"
        elif self.tipo==TIPOS.BOOLEANO:
            ret="Bool"
        elif self.tipo==TIPOS.DECIMAL:
            ret="Float64"
        elif self.tipo==TIPOS.ENTERO:
            ret="Int64"
        elif self.tipo==TIPOS.ARREGLO:
            ret="Arreglo"
        elif self.tipo==TIPOS.CHARACTER:
            ret="Char"
        return ret