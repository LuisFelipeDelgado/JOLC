class Arbol:
    def __init__(self, instrucciones ):
        self.instrucciones = instrucciones
        self.funciones = []
        self.excepciones = []
        self.tablas = []
        self.consola = ""
        self.TSglobal = None
        self.dot = ""
        self.contador = 0
        self.raiz = None

    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

    def getExcepciones(self):
        return self.excepciones

    def setExcepciones(self, excepciones):
        self.excepciones = excepciones

    def getConsola(self):
        return self.consola
    
    def setConsola(self, consola):
        self.consola = consola

    def updateConsola(self,cadena):
        self.consola += str(cadena) + '\n'

    def updateConsola2(self,cadena):
        self.consola += str(cadena)

    def getTSGlobal(self):
        return self.TSglobal

    def setTSglobal(self, TSglobal):
        self.TSglobal = TSglobal

    def getFunciones(self):
        return self.funciones

    def getFuncion(self, nombre):
        for funcion in self.funciones:
            if funcion.nombre == nombre:
                return funcion
        return None

    def addFuncion(self, funcion):
        self.funciones.append(funcion)

    def getDot(self, raiz): ## DEVUELVE EL STRING DE LA GRAFICA EN GRAPHVIZ
        self.dot = ""
        self.dot += "digraph {\n"
        self.dot += "graph [fontname = arial, fontcolor=lime, bgcolor=transparent];\n"
        self.dot += "node [fontname = arial, fontcolor=lime, color=lime];\n"
        self.dot += "edge [fontname = arial, fontcolor=lime, color=lime];\n"
        self.dot += "n0[label=\"" + raiz.getValor().replace("\"", "\\\"") + "\"];\n"
        self.contador = 1
        self.recorrerAST("n0", raiz)
        self.dot += "}"
        return self.dot

    def recorrerAST(self, idPadre, nodoPadre):
        for hijo in nodoPadre.getHijos():
            nombreHijo = "n" + str(self.contador)
            self.dot += nombreHijo + "[label=\"" + hijo.getValor().replace("\"", "\\\"") + "\"];\n"
            self.dot += idPadre + "->" + nombreHijo + ";\n"
            self.contador += 1
            self.recorrerAST(nombreHijo, hijo)

    def tablaSE(self):
        listtmp3 = []
        listtmp = []
        listtmp.append("digraph {\n")
        listtmp.append("graph [fontname = arial, fontcolor=springgreen, bgcolor=transparent];\n")
        listtmp.append("node [fontname = arial, fontcolor=white, color=springgreen];\n")
        listtmp.append("simbolos [shape=none, margin=0, label=<\n")
        listtmp.append('<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">\n')
        listtmp.append('<TR><TD BGCOLOR="springgreen"><FONT FACE="arial">Tipo</FONT></TD><TD BGCOLOR="springgreen"><FONT FACE="arial">Descripcion</FONT></TD><TD BGCOLOR="springgreen"><FONT FACE="arial">Linea</FONT></TD><TD BGCOLOR="springgreen"><FONT FACE="arial">Columna</FONT></TD><TD BGCOLOR="springgreen"><FONT FACE="arial">Tiempo</FONT></TD></TR>\n')
        for m in self.excepciones:
            listtmp3.append('<TR><TD><FONT FACE="arial">' + m.tipo + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">'+ m.descripcion +'</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + str(m.linea) + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + str(m.columna) + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + m.tiempo + '</FONT></TD></TR>\n')
        listtmp2 = set(listtmp3)
        listtmp = listtmp + list(listtmp2)
        listtmp.append("</TABLE>>];\n")
        listtmp.append("}")
        tabs2 = ""
        for m in listtmp:
            tabs2 += m
        return tabs2

    def tablaS(self):
        listtmp3 = []
        listtmp = []
        listtmp.append("digraph {\n")
        listtmp.append("graph [fontname = arial, fontcolor=plum1, bgcolor=transparent];\n")
        listtmp.append("node [fontname = arial, fontcolor=white, color=plum1];\n")
        listtmp.append("simbolos [shape=none, margin=0, label=<\n")
        listtmp.append('<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">\n')
        listtmp.append('<TR><TD BGCOLOR="plum1"><FONT FACE="arial">Identificador</FONT></TD><TD BGCOLOR="plum1"><FONT FACE="arial">Tipo</FONT></TD><TD BGCOLOR="plum1"><FONT FACE="arial">Entorno</FONT></TD><TD BGCOLOR="plum1"><FONT FACE="arial">Linea</FONT></TD><TD BGCOLOR="plum1"><FONT FACE="arial">Columna</FONT></TD></TR>\n')
        for m in self.tablas:
            for n, value in m.tabla.items():
                if isinstance(value.valor,dict):
                    listtmp3.append('<TR><TD><FONT FACE="arial">' + n + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">Struct</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + m.getEntorno() + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + str(value.fila) + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + str(value.columna) + '</FONT></TD></TR>\n')
                elif isinstance(value.valor,list):
                    listtmp3.append('<TR><TD><FONT FACE="arial">' + n + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">Arreglo</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + m.getEntorno() + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + str(value.fila) + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + str(value.columna) + '</FONT></TD></TR>\n')
                else:
                    listtmp3.append('<TR><TD><FONT FACE="arial">' + n + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + value.tipo.name + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + m.getEntorno() + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + str(value.fila) + '</FONT></TD>' +
                                '<TD ><FONT FACE="arial">' + str(value.columna) + '</FONT></TD></TR>\n')
        listtmp2 = set(listtmp3)
        listtmp = listtmp + list(listtmp2)
        listtmp.append("</TABLE>>];\n")
        listtmp.append("}")
        tabs2 = ""
        for m in listtmp:
            tabs2 += m
        return tabs2

    def getTabla(self):
        return self.tablas