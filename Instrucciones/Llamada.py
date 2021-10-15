from Instrucciones.Return import Return
from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo
from Instrucciones.Funcion import Funcion
from Excepciones.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from TS.Tipo import TIPOS
import copy

class Llamada(Expresion):
    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table):
        result = table.getVariable(self.nombre) ## OBTENER LA FUNCION
        if result == None: # NO SE ENCONTRO LA FUNCION
            return Excepcion("Semantico", "NO SE ENCONTRO EL IDENTIFICADOR: " + self.nombre, self.fila, self.columna)
        # OBTENER PARAMETROS
        if result.tipo==TIPOS.FUNCION:
            nuevaTabla = TablaSimbolos(table)
            nuevaTabla.setEntorno("FUNCION"+self.nombre)
            if len(result.valor[0]) != len(self.parametros): #LA CANTIDAD DE PARAMETROS ES LA ADECUADA
                return Excepcion("Semantico", "Cantidad de Parametros incorrecta.", self.fila, self.columna)
            contador=0
            if len(result.valor[0])>0:
                for expresion in self.parametros: # SE OBTIENE EL VALOR DEL PARAMETRO EN LA LLAMADA
                    resultExpresion = expresion.interpretar(tree, table)
                    identificador = result.valor[0][contador]
                    if isinstance(resultExpresion, Excepcion): return resultExpresion
                    if not isinstance(resultExpresion,dict):
                        simbolo = Simbolo(resultExpresion.tipo, identificador, self.fila, self.columna, resultExpresion)
                    else:
                        simbolo = Simbolo(TIPOS.STRUCT, identificador, self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setVariable(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla
                    contador += 1
            
            if None in result.valor[1]:
                result.valor[1].remove(None)
            for instruccion in result.valor[1]:
                instrresult = instruccion.interpretar(tree,nuevaTabla)
                if isinstance(instrresult, Excepcion):
                    tree.getExcepciones().append(instrresult)
                    tree.updateConsola(instrresult.toString())
                if isinstance(instrresult, Return):
                    if instrresult.result==None:
                        return
                    if isinstance(instrresult.result, dict):
                        retorno=instrresult.result
                    else:
                        retorno = instrresult.result.interpretar(tree,nuevaTabla)
                    return retorno
        elif result.tipo==TIPOS.STRUCT:
            dicts = copy.deepcopy(result.valor)
            if len(dicts['atributos']) != len(self.parametros):
                return Excepcion("Semantico", "Cantidad de Parametros incorrecta.", self.fila, self.columna)
            contador=0
            for i in dicts['atributos']:
                tmp = self.parametros[contador].interpretar(tree,table)
                dicts['atributos'][i]=tmp
                contador = contador+1
            return dicts
    def getNodo(self):
        nodo1 = NodoAST("LLAMADA")
        nodoi = NodoAST("IDENTIFICADOR")
        nodoi.agregarHijo(str(self.nombre))
        nodo1.agregarHijoNodo(nodoi)
        nodo1.agregarHijo("(")
        if len(self.parametros)>0:
            nodo = NodoAST("PARAMETROS")
            for i in self.parametros:
                if i == self.parametros[0]:
                    instruccioness3 = NodoAST("PARAMETRO")
                    instruccioness3.agregarHijoNodo(i.getNodo())
                    nodo.agregarHijoNodo(instruccioness3)
                else:
                    instrtmp = nodo
                    instruccioness3 = NodoAST("PARAMETRO")
                    nodo = NodoAST("PARAMETROS")
                    nodo.agregarHijoNodo(instrtmp)
                    nodo.agregarHijo(",")
                    instruccioness3.agregarHijoNodo(i.getNodo())
                    nodo.agregarHijoNodo(instruccioness3)
            nodo1.agregarHijoNodo(nodo)
        nodo1.agregarHijo(")")
        return nodo1