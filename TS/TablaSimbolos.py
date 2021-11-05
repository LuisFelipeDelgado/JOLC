from Excepciones.Excepcion import Excepcion


class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {}
        self.funciones = {}
        self.structs = {}
        self.anterior = anterior
        self.tipo = None
        self.entorno = ""
        self.tamano = 0
        self.breakE = ''
        self.continueE = ''
        self.returnE = ''
        if anterior!=None:
            self.tamano = self.anterior.tamano
            self.breakE = self.anterior.breakE
            self.continueE = self.anterior.continueE
            self.returnE = self.anterior.returnE
        self.funcion = False

    def setVariable(self, simbolo):      # Agregar una variable
        if simbolo in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id] = simbolo
            return None

    def getVariable(self, id):            # obtener una variable
        tablaActual = self
        while tablaActual != None:
            if id in tablaActual.tabla:
                return tablaActual.tabla[id]           # RETORNA SIMBOLO
            else:
                tablaActual = tablaActual.anterior
        return None

    def setFuncion(self, id, simbolo): 
        if id in self.funciones :
            return Excepcion("Semantico", "Funcion " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.funciones[id] = simbolo

    def getFuncion(self, id):            # obtener una variable
        tablaActual = self
        while tablaActual != None:
            if id in tablaActual.funciones:
                return tablaActual.funciones[id]           # RETORNA SIMBOLO
            else:
                tablaActual = tablaActual.anterior
        return None

    def setStruct(self, id, simbolo): 
        if id in self.structs :
            return Excepcion("Semantico", "Funcion " + id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.structs[id] = simbolo

    def getStruct(self, id):            # obtener una variable
        tablaActual = self
        while tablaActual != None:
            if id in tablaActual.structs:
                return tablaActual.structs[id]           # RETORNA SIMBOLO
            else:
                tablaActual = tablaActual.anterior
        return None

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id in tablaActual.tabla :
                tablaActual.tabla[simbolo.id].setValor(simbolo.getValor())
                tablaActual.tabla[simbolo.id].setTipo(simbolo.getTipo())
                return tablaActual.tabla[simbolo.id]
            else:
                tablaActual = tablaActual.anterior
        self.tamano+=1
        self.tabla[simbolo.id] = simbolo
        return self.tabla[simbolo.id]
        
    def getTable(self):
        return self.tabla

    def getAnterior(self):
        return self.anterior

    def setAnterior(self, Anterior):
        self.anterior = Anterior

    def setEntorno(self, nombre):
        self.entorno = nombre

    def getEntorno(self):
        return self.entorno