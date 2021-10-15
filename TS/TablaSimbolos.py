from Excepciones.Excepcion import Excepcion


class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior
        self.tipo = None
        self.entorno = ""
        self.tamano = 0
        if anterior!=None:
            self.tamano = self.anterior.tamano

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

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id in tablaActual.tabla :
                tablaActual.tabla[simbolo.id].setValor(simbolo.getValor())
                return None             # simbolo actualizado
            else:
                tablaActual = tablaActual.anterior
        
        self.tabla[simbolo.id] = simbolo
        return None # --> simbolo agregado
        
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