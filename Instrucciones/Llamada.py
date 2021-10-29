from Instrucciones.Return import ReturnI
from Abstract.ReturnA import Return
from Abstract.instruccion import Expresion
from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo
from Instrucciones.Funcion import Funcion
from Excepciones.Excepcion import Excepcion
from TS.TCI import TCI
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
        result = table.getFuncion(self.nombre) ## OBTENER LA FUNCION
        # OBTENER PARAMETROS
        if result != None:
            paramValues = []
            codigoAux = TCI()
            codigoR = codigoAux.getInstance()
            tamano = table.tamano
            for param in self.parametros:
                if table.funcion and isinstance(param,Llamada):
                    codigoR.addComment("Guardar Temp----------------------------------------")
                    tempP1 = codigoR.temps[-1]
                    tempP = codigoR.addTemp()
                    codigoR.addExp(tempP,'P',table.tamano,'+')
                    codigoR.setStack(tempP,tempP1)
                    table.tamano += 1
                    paramValues.append(param.interpretar(tree,table))
                    codigoR.addComment("RECUPERAR Temp--------------------------------------")
                    table.tamano -= 1
                    tempP = codigoR.addTemp()
                    codigoR.addExp(tempP,'P',table.tamano,'+')
                    codigoR.getStack(tempP1,tempP)
                else:
                    paramValues.append(param.interpretar(tree,table))
            temp = codigoR.addTemp()

            codigoR.addExp(temp, 'P', tamano+1, '+')
            aux = 0
            for param in paramValues:
                aux = aux +1
                codigoR.setStack(temp, param.valor)
                if aux != len(paramValues):
                    codigoR.addExp(temp, temp, '1', '+')
                
            codigoR.newEnv(tamano)
            codigoR.callFun(self.nombre)
            codigoR.getStack(temp, 'P')
            codigoR.retEnv(tamano)
            if False:
                return
            elif result.tipo == TIPOS.BOOLEANO:
                ev = codigoR.newE()
                ef = codigoR.newE()
                codigoR.addIf(temp,'1','==',ev)
                codigoR.GoTo(ef)
                ret = Return(None,TIPOS.BOOLEANO,False)
                ret.ev = ev
                ret.ef = ef
                return ret
            return Return(temp, result.tipo, True,result.tipos)
            '''nuevaTabla = TablaSimbolos(table)
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
                    return retorno'''
        else:
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